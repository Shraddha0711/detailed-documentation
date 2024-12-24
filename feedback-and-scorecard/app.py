# Import required libraries and modules
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from customer_agent import customer_graph  # Import the customer graph logic
from sales_agent import sales_graph  # Import the sales graph logic
import uvicorn  # ASGI server to run the FastAPI app
import firebase_admin  # Firebase admin SDK
from firebase_admin import credentials, firestore  # Firestore client for database interactions
import os  # For interacting with environment variables
import json  # For working with JSON data
from dotenv import load_dotenv  # Load environment variables from a .env file

# Load environment variables from a .env file
load_dotenv()

# Initialize Firebase credentials using the provided certificate path
cred = credentials.Certificate(os.getenv("CRED_PATH"))
firebase_admin.initialize_app(cred)  # Initialize the Firebase app
db = firestore.client()  # Initialize the Firestore database client

# Initialize the FastAPI app
app = FastAPI()

# Enable Cross-Origin Resource Sharing (CORS) to allow requests from different origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Configuration for the agents, including unique identifiers
config = {
    "thread_id": "main",  # Thread ID for tracking requests
    "checkpoint_ns": "my_namespace",  # Namespace for checkpoints
    "checkpoint_id": "my_checkpoint",  # Unique checkpoint identifier
}

# Global variable to store the compiled customer graph
customer_compiled_graph = None

def get_customer_compiled_graph():
    """
    Returns the compiled customer graph. If it hasn't been compiled yet,
    it loads it from the customer_graph module.
    """
    global customer_compiled_graph
    if customer_compiled_graph is None:
        customer_compiled_graph = customer_graph  # Load the customer graph if not loaded
    return customer_compiled_graph


# Global variable to store the compiled sales graph
sales_compiled_graph = None

def get_sales_compiled_graph():
    """
    Returns the compiled sales graph. If it hasn't been compiled yet,
    it loads it from the sales_graph module.
    """
    global sales_compiled_graph
    if sales_compiled_graph is None:
        sales_compiled_graph = sales_graph  # Load the sales graph if not loaded
    return sales_compiled_graph


def generate_scorecard(transcript, type):
    """
    Generates a scorecard based on the provided transcript and type (customer or sales).
    The function processes the transcript, invokes the appropriate agent, 
    and returns a detailed feedback scorecard.
    """
    context = ""  # Variable to store system context
    conversation = []  # List to store conversation entries
    
    # Process each entry in the transcript
    for entry in transcript:
        if entry["role"] == "system":
            context = entry["content"]  # Extract system context
        else:
            conversation.append(f"{entry['role']}: {entry['content']}")  # Append user/system conversation

    # Combine context and conversation into a single formatted transcript
    formatted_transcript = f"Context:\n{context}\n\nConversation:\n" + "\n".join(conversation)

    # If the type is 'customer', use the customer graph for processing
    if type == "customer":
        graph = get_customer_compiled_graph()
        result = graph.invoke({"transcript": formatted_transcript}, config=config)
        result.pop("transcript")  # Remove the transcript from the result
        result = {item.split(':', 1)[0].strip(): item.split(':', 1)[1].strip() for item in result['aggregate']}  # Format results
        # Return detailed scorecard for customer interaction
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
                "customer_satisfaction_score": result["customer_satisfaction_score"],
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
            "feedback": json.loads(result["feedback"])
        }

    # If the type is 'sales', use the sales graph for processing
    elif type == "sales":
        graph = get_sales_compiled_graph()
        result = graph.invoke({"transcript": formatted_transcript}, config=config)
        result.pop("transcript")
        result = {item.split(':', 1)[0].strip(): item.split(':', 1)[1].strip() for item in result['aggregate']}
        # Return detailed scorecard for sales interaction
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
            "feedback": json.loads(result["feedback"])
        }
    else:
        raise ValueError("Invalid type provided")

# Define the FastAPI endpoint to retrieve scorecard based on transcription ID
@app.post("/get_scorecard")
async def get_transcription(room_id: str):
    try:
        # Check if feedback already exists in Firestore
        feedback_doc_ref = db.collection(u'feedback').document(room_id)
        feedback_doc = feedback_doc_ref.get()
        
        if feedback_doc.exists:
            # If feedback exists, return the existing feedback
            return feedback_doc.to_dict()
        else:
            # Retrieve the transcription document from Firestore
            doc_ref = db.collection(u'Transcription').document(room_id)
            doc = doc_ref.get()
            
            if doc.exists:
                transcript = doc.to_dict()["transcript"]
                type = doc.to_dict()["type"]

                # Ensure the type is valid (either customer or sales)
                if type in ["customer", "sales"]:
                    # Generate feedback based on the transcript and type
                    feedback = generate_scorecard(transcript, type)
                    
                    # Store the feedback in Firestore for future reference
                    feedback_doc_ref.set(feedback)
                    
                    # Return the generated feedback
                    return feedback
                else:
                    return {"error": "Invalid type"}    
            else:
                # If transcription is not found, raise 404 error
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Transcription not found"
                )
    except Exception as e:
        # If there's an error, return a 500 Internal Server Error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve transcription: {str(e)}"
        )

# Run the FastAPI application using uvicorn
if __name__ == "__main__":
    uvicorn.run(app, port=8000)
