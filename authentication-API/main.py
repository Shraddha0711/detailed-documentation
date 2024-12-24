# Importing necessary libraries
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt  # For JWT token handling
from datetime import datetime, timedelta
from typing import Optional
from pydantic import BaseModel, EmailStr  # For data validation
import firebase_admin
from firebase_admin import credentials, firestore  # For Firebase Firestore database
from passlib.context import CryptContext  # For password hashing and verification
import os
from dotenv import load_dotenv  # For loading environment variables

# Load environment variables from .env file
load_dotenv()

# Firebase initialization with credentials loaded from environment variable
cred = credentials.Certificate(os.getenv("CRED_PATH"))  # Path to the Firebase credentials file
firebase_admin.initialize_app(cred)  # Initialize Firebase app
db = firestore.client()  # Firestore client for database operations

# JWT Configuration
SECRET_KEY = os.getenv("SECRET_KEY")  # Secret key for encoding and decoding JWTs
ALGORITHM = "HS256"  # Algorithm used for encoding JWTs
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Token expiration time in minutes

# FastAPI app initialization
app = FastAPI()

# CORS Middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (can be customized for security)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# OAuth2PasswordBearer defines the token URL for authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")  # For bcrypt password hashing

# Pydantic Models for request validation
class UserBase(BaseModel):
    email: EmailStr  # Email must be a valid email address
    full_name: Optional[str] = None  # Optional full name field

class UserCreate(UserBase):
    password: str  # Password is required for user creation

class User(UserBase):
    id: str  # User ID from Firestore
    disabled: bool = False  # Indicates if the user is active or disabled
    created_at: datetime  # Timestamp when the user was created

    class Config:
        from_attributes = True  # Allow user data mapping from Firestore attributes

class UserInDB(User):
    hashed_password: str  # Store hashed password in the database

class Token(BaseModel):
    access_token: str  # The JWT access token
    token_type: str  # Type of token (usually "bearer")

class TokenData(BaseModel):
    email: Optional[str] = None  # Data stored in the JWT payload (in this case, user's email)

# Password hashing utilities
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)  # Verify plain password with hashed password

def get_password_hash(password):
    return pwd_context.hash(password)  # Hash password using bcrypt

# Database Operations with Firestore

async def get_user_by_email(email: str) -> Optional[UserInDB]:
    """Fetch a user from Firestore by email."""
    users_ref = db.collection('users')
    query = users_ref.where('email', '==', email).limit(1)  # Query for the user with the given email
    users = query.get()  # Execute the query
    
    for user in users:
        user_data = user.to_dict()  # Convert Firestore document to dictionary
        user_data['id'] = user.id  # Add user document ID
        return UserInDB(**user_data)  # Return the user as UserInDB model
    return None  # Return None if no user is found

async def create_user_in_db(user: UserCreate) -> UserInDB:
    """Create a new user in Firestore database."""
    users_ref = db.collection('users')
    
    # Check if user already exists based on email
    if await get_user_by_email(user.email):
        raise HTTPException(
            status_code=400,
            detail="Email already registered"  # Raise error if email already exists
        )
    
    # Create user data with hashed password and other details
    user_data = {
        "email": user.email,
        "full_name": user.full_name,
        "hashed_password": get_password_hash(user.password),
        "disabled": False,  # User is active by default
        "created_at": datetime.utcnow()  # Record current time as creation time
    }
    
    # Add user data to Firestore
    doc_ref = users_ref.add(user_data)
    user_data['id'] = doc_ref[1].id  # Assign the Firestore document ID to the user data
    
    return UserInDB(**user_data)  # Return user as UserInDB model

# JWT Functions

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create JWT token for the user."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta  # Set token expiration if provided
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)  # Default expiration time
    
    to_encode.update({"exp": expire})  # Add expiration field to token data
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)  # Encode token with secret key
    return encoded_jwt  # Return the encoded JWT

async def authenticate_user(email: str, password: str):
    """Authenticate user by verifying email and password."""
    user = await get_user_by_email(email)  # Retrieve user from Firestore by email
    if not user:
        return False  # User does not exist
    if not verify_password(password, user.hashed_password):
        return False  # Password does not match the stored hash
    return user  # Return the authenticated user

async def get_current_user(token: str = Depends(oauth2_scheme)):
    """Get the current authenticated user based on the JWT token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])  # Decode the token
        email: str = payload.get("sub")  # Get email from token's subject field
        if email is None:
            raise credentials_exception  # Raise error if email is not found in token
        token_data = TokenData(email=email)  # Create TokenData model
    except JWTError:
        raise credentials_exception  # Raise error if JWT is invalid or expired

    user = await get_user_by_email(token_data.email)  # Fetch user from Firestore
    if user is None:
        raise credentials_exception  # Raise error if user does not exist
    return user  # Return the user object

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    """Ensure the user is active before allowing access."""
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")  # Raise error if user is disabled
    return current_user  # Return the active user

# API Endpoints

@app.post("/signup", response_model=User)
async def signup(user: UserCreate):
    """Create a new user via signup endpoint."""
    try:
        db_user = await create_user_in_db(user)  # Create user in the database
        return db_user  # Return the created user
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)  # Raise error if something goes wrong during user creation
        )

@app.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Login user and generate JWT token."""
    user = await authenticate_user(form_data.username, form_data.password)  # Authenticate user
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",  # Invalid credentials
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token with expiration time
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}  # Return the JWT token

@app.get("/users/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    """Get the currently logged-in user's information."""
    return current_user  # Return the current active user

@app.put("/users/me", response_model=User)
async def update_user(
    updated_user: UserBase,
    current_user: User = Depends(get_current_active_user)
):
    """Update the current user's information."""
    try:
        user_ref = db.collection('users').document(current_user.id)  # Reference to Firestore document
        user_ref.update({
            "full_name": updated_user.full_name,  # Update full name
            "email": updated_user.email  # Update email
        })
        
        # Get updated user data
        updated_data = user_ref.get().to_dict()
        updated_data['id'] = current_user.id
        return User(**updated_data)  # Return updated user data
    
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)  # Raise error if update fails
        )

@app.delete("/users/me")
async def delete_user(current_user: User = Depends(get_current_active_user)):
    """Delete the current user's account."""
    try:
        db.collection('users').document(current_user.id).delete()  # Delete user from Firestore
        return {"message": "User deleted successfully"}  # Return success message
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)  # Raise error if deletion fails
        )

# Run the FastAPI application with uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
