# Importing necessary libraries and modules
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from customer_agent import customer_graph
from sales_agent import sales_graph
import uvicorn
import firebase_admin
from firebase_admin import credentials, firestore
import os
import json
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Initialize Firebase app with credentials
cred = credentials.Certificate(os.getenv("CRED_PATH"))
firebase_admin.initialize_app(cred)
db = firestore.client()  # Initialize Firestore client

# Create FastAPI app instance
app = FastAPI()

# Enable CORS for the app to allow requests from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow requests from all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all HTTP headers
)

# Configuration settings for graph processing
config = {
    "thread_id": "main",  # Identifier for the thread
    "checkpoint_ns": "my_namespace",  # Namespace for checkpoints
    "checkpoint_id": "my_checkpoint",  # Unique identifier for checkpoint
}

# Global variable to store the compiled graph for customer interactions
customer_compiled_graph = None

# Function to retrieve and cache the compiled customer graph
def get_customer_compiled_graph():
    global customer_compiled_graph
    if customer_compiled_graph is None:
        customer_compiled_graph = customer_graph  # Load the graph if not already loaded
    return customer_compiled_graph

# Global variable to store the compiled graph for sales interactions
sales_compiled_graph = None

# Function to retrieve and cache the compiled sales graph
def get_sales_compiled_graph():
    global sales_compiled_graph
    if sales_compiled_graph is None:
        sales_compiled_graph = sales_graph  # Load the graph if not already loaded
    return sales_compiled_graph

# Function to generate a scorecard based on a transcription, prompt type, and other parameters
def generate_scorecard(transcript, prompt_type, duration, user_id):
    # Extract context and conversation from the transcription
    context = ""
    conversation = []
    for entry in transcript:
        if entry["role"] == "system":
            context = entry["content"]
        else:
            conversation.append(f"{entry['role']}: {entry['content']}")

    # Format the transcript for processing
    formatted_transcript = f"Context:\n{context}\n\nConversation:\n" + "\n".join(conversation)

    # Determine the appropriate graph to use based on the prompt type
    if prompt_type == "customer":
        graph = get_customer_compiled_graph()
        result = graph.invoke({"transcript": formatted_transcript}, config=config)
        result.pop("transcript")  # Remove transcript from results
        result = {item.split(':', 1)[0].strip(): item.split(':', 1)[1].strip() for item in result['aggregate']}
        
        # Format the result into a structured scorecard
        return {
            "communication_and_delivery": {
                "empathy_score": result["empathy_score"],
                "clarity_and_conciseness": result["clarity_and_conciseness"],
                "grammar_and_language": result["grammar_and_language"],
                "listening_score": result["listening_score"],
                "positive_sentiment_score": result["positive_sentiment_score"],
                "structure_and_flow": result["structure_and_flow"],
                "stuttering_words": result["stuttering_words"],   
                "active_listening_skills": result["active_listening_skills"]
            },
            "customer_interaction_and_resolution": {
                "problem_resolution_effectiveness": result["problem_resolution_effectiveness"],
                "personalisation_index": result["personalisation_index"],
                "conflict_management": result["conflict_management"],
                "response_time": result["response_time"],
                "customer_satisfaction_score": result["customer_satisfiction_score"],
                "rapport_building": result["rapport_building"],
                "engagement": result["engagement"]
            },
            "sales_and_persuasion": {
                "product_knowledge_score": None,
                "persuasion_and_negotiation_skills": None,
                "objection_handling": None,
                "upselling_success_rate": None,
                "call_to_action_effectiveness": None,
                "questioning_technique": None
            },
            "professionalism_and_presentation": {
                "confidence_score": None,
                "value_proposition": None,
                "pitch_quality": None
            },
            "feedback": json.loads(result["feedback"]),
            "duration": duration,
            "user_id": user_id,
            "timestamp": datetime.utcnow()
        }
    elif prompt_type == "sales":
        graph = get_sales_compiled_graph()
        result = graph.invoke({"transcript": formatted_transcript}, config=config)
        result.pop("transcript")  # Remove transcript from results
        result = {item.split(':', 1)[0].strip(): item.split(':', 1)[1].strip() for item in result['aggregate']}
        
        # Format the result into a structured scorecard
        return {
            "communication_and_delivery": {
                "empathy_score": None,
                "clarity_and_conciseness": None,
                "grammar_and_language": None,
                "listening_score": None,
                "positive_sentiment_score": None,
                "structure_and_flow": None,
                "stuttering_words": None,
                "active_listening_skills": None
            },
            "customer_interaction_and_resolution": {
                "problem_resolution_effectiveness": None,
                "personalisation_index": None,
                "conflict_management": None,
                "response_time": None,
                "customer_satisfaction_score": None,
                "rapport_building": None,
                "engagement": None
            },
            "sales_and_persuasion": {
                "product_knowledge_score": result["product_knowledge_score"],
                "persuasion_and_negotiation_skills": result["persuasion_and_negotiation_skills"],
                "objection_handling": result["objection_handling"],
                "upselling_success_rate": result["upselling_success_rate"],
                "call_to_action_effectiveness": result["call_to_action_effectiveness"],
                "questioning_technique": result["questioning_technique"]
            },
            "professionalism_and_presentation": {
                "confidence_score": result["confidence_score"],
                "value_proposition": result["value_proposition"],
                "pitch_quality": result["pitch_quality"]
            },
            "feedback": json.loads(result["feedback"]),
            "duration": duration,
            "user_id": user_id,
            "timestamp": datetime.utcnow()
        }
    else:
        raise ValueError("Invalid type provided")

# API endpoint to retrieve or generate a scorecard for a transcription
@app.post("/get_scorecard")
async def get_transcription(room_id: str):
    try:
        # Check if feedback already exists in the 'feedback' collection
        feedback_doc_ref = db.collection(u'feedback').document(room_id)
        feedback_doc = feedback_doc_ref.get()
        
        if feedback_doc.exists:
            # Return existing feedback
            return feedback_doc.to_dict()
        else:
            # Retrieve transcription document from Firestore
            doc_ref = db.collection(u'Transcription').document(room_id)
            doc = doc_ref.get()

            if doc.exists:
                doc_data = doc.to_dict()
                transcript = doc_data["transcript"]
                prompt_type = doc_data["type"]
                duration = doc_data.get("call_duration", None)  # Default to None if not present
                user_id = doc_data.get("user_id", None)  # Default to None if not present

                # Validate the prompt type
                if prompt_type in ["customer", "sales"]:
                    # Generate feedback scorecard
                    feedback = generate_scorecard(transcript, prompt_type, duration, user_id)
                    
                    # Store feedback in Firestore 'feedback' collection
                    feedback_doc_ref.set(feedback)
                    
                    # Return the generated feedback
                    return feedback
                else:
                    return {"error": "Invalid type"}    
            else:
                # Handle case when transcription is not found
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Transcription not found"
                )
    except Exception as e:
        # Handle server-side exceptions
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve transcription: {str(e)}"
        )

# Entry point to run the FastAPI app
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
