
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import firebase_admin
from firebase_admin import credentials, firestore, initialize_app
from typing import List
from pydantic import BaseModel
import os
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Firebase

cred = credentials.Certificate(os.getenv("CRED_PATH"))
firebase_admin.initialize_app(cred)
db = firestore.client()

@app.get("/feedback/{user_id}")
async def get_feedback(user_id: str):
    try:
        feedbacks = db.collection('feedback').where('user_id', '==', user_id).stream()
        feedback_list = [doc.to_dict() for doc in feedbacks]
        
        if not feedback_list:
            raise HTTPException(status_code=404, detail="No feedback found")
            
        return feedback_list
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
