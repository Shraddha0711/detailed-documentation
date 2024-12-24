from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
import uuid
import firebase_admin
from firebase_admin import firestore, credentials
import os
import uvicorn
import random
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Initialize Firebase using credentials stored in the environment variable
cred = credentials.Certificate(os.getenv("CRED_PATH"))
firebase_admin.initialize_app(cred)

# Create a Firestore client to interact with Firebase Firestore database
db = firestore.client()

# Initialize FastAPI application
app = FastAPI()

# Add middleware for Cross-Origin Resource Sharing (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (you may restrict this later for security)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Endpoint to create a new scenario
@app.post("/scenarios", status_code=status.HTTP_201_CREATED)
async def create_scenario(name: str, prompt: str, type: str, AI_persona: str):
    """
    This endpoint creates a new scenario with the provided details. 
    It generates a unique ID for the scenario and stores it in Firestore.
    """
    id = str(uuid.uuid4())  # Generate a unique ID for the new scenario
    try:
        # Reference the "scenarios" collection in Firestore and create a new document
        doc_ref = db.collection(u'scenarios').document(id)
        doc_ref.set({
            u'name': name,
            u'prompt': prompt,
            u'type': type,
            u'persona': AI_persona
        })
        return {"message": f"Scenario created successfully", "id": id}
    except Exception as e:
        # If an error occurs during the creation process, raise an HTTP 500 error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create scenario: {str(e)}"
        )

# Endpoint to get a specific scenario based on roleplay type and difficulty level
@app.get("/scenarios/{scenario_id}")
async def get_scenario(roleplay_type: str, difficulty_level: str):
    """
    This endpoint retrieves a scenario from Firestore based on the specified roleplay type
    and difficulty level. It randomly selects one scenario if there are multiple matching.
    """
    # Query Firestore for scenarios that match the specified roleplay type
    scenarios_ref = db.collection(u'scenarios')
    query = scenarios_ref.where("type", "==", roleplay_type)
    docs = query.stream()
    
    # Collect all scenario IDs that match the type (e.g., "sales")
    sales_scenarios = []
    for doc in docs:
        sales_scenarios.append(doc.id)

    # Randomly select a scenario from the matching ones
    selected_scenario = random.choice(sales_scenarios)

    # Retrieve the selected scenario's document from Firestore
    doc_ref = db.collection(u'scenarios').document(selected_scenario)
    doc = doc_ref.get()
    
    if doc.exists:
        scenario = doc.to_dict()
        
        # Return the scenario details based on the difficulty level
        if difficulty_level == "easy":
            return {
                "name": scenario.get('name', ''),
                "prompt": scenario.get("easy_prompt", ""),
                "persona_name": scenario.get('persona_name', ''),
                "persona": scenario.get('persona', ''),
                "difficulty_level": difficulty_level,
                "image_url": scenario.get('image_url', ''),
                "voice_id": scenario.get('voice_id', ''),
                "type": scenario.get('type', '')
            }
        elif difficulty_level == "medium":
            return {
                "name": scenario.get('name', ''),
                "prompt": scenario.get("medium_prompt", ""),
                "persona_name": scenario.get('persona_name', ''),
                "persona": scenario.get('persona', ''),
                "difficulty_level": difficulty_level,
                "image_url": scenario.get('image_url', ''),
                "voice_id": scenario.get('voice_id', ''),
                "type": scenario.get('type', '')
            }
        elif difficulty_level == "hard":
            return {
                "name": scenario.get('name', ''),
                "prompt": scenario.get("hard_prompt", ""),
                "persona_name": scenario.get('persona_name', ''),
                "persona": scenario.get('persona', ''),
                "difficulty_level": difficulty_level,
                "image_url": scenario.get('image_url', ''),
                "voice_id": scenario.get('voice_id', ''),
                "type": scenario.get('type', '')
            }

# Endpoint to update an existing scenario based on scenario ID
@app.put("/scenarios/{scenario_id}")
async def update_scenario(scenario_id: str, name: str, prompt: str, type: str, AI_persona: str):
    """
    This endpoint allows updating an existing scenario's details using the scenario ID.
    It verifies the scenario exists before updating.
    """
    try:
        doc_ref = db.collection(u'scenarios').document(scenario_id)
        doc = doc_ref.get()
        if not doc.exists:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Scenario not found"
            )
        # Update the scenario with the new values
        doc_ref.update({
            u'name': name,
            u'prompt': prompt,
            u'type': type,
            u'persona': AI_persona
        })
        return {"message": "Scenario updated successfully"}
    except HTTPException:
        raise
    except Exception as e:
        # If an error occurs during the update, raise an HTTP 500 error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update scenario: {str(e)}"
        )

# Endpoint to delete an existing scenario by its ID
@app.delete("/scenarios/{scenario_id}")
async def delete_scenario(scenario_id: str):
    """
    This endpoint allows deleting a scenario by its unique ID.
    It checks if the scenario exists before attempting to delete.
    """
    try:
        doc_ref = db.collection(u'scenarios').document(scenario_id)
        doc = doc_ref.get()
        if not doc.exists:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Scenario not found"
            )
        # Delete the scenario document from Firestore
        doc_ref.delete()
        return {"message": "Scenario deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        # If an error occurs during the deletion, raise an HTTP 500 error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete scenario: {str(e)}"
        )

# Endpoint to get a list of all scenario IDs in the database
@app.get("/scenarios")
async def get_all_scenario_ids():
    """
    This endpoint retrieves all scenario IDs from the Firestore database.
    It returns an empty message if no scenarios are found.
    """
    try:
        docs = db.collection(u'scenarios').stream()
        
        # Collect all the scenario IDs
        scenario_ids = [doc.id for doc in docs]
        
        if scenario_ids:
            return {"scenario_ids": scenario_ids}
        else:
            return {"message": "No scenarios found"}
        
    except Exception as e:
        # If an error occurs while fetching scenarios, raise an HTTP 500 error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve scenarios: {str(e)}"
        )

# Start the FastAPI application using Uvicorn server
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
