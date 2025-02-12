from fastapi import FastAPI, HTTPException, Query
import firebase_admin
from firebase_admin import credentials, firestore
import openai  # Use OpenAI API (replace with your LLM API)
from google.api_core.exceptions import GoogleAPICallError
from fastapi.middleware.cors import CORSMiddleware
import os
import json
# from dotenv import load_dotenv
# load_dotenv()
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



# OpenAI API Key (Replace with your API)
openai.api_key = os.getenv("OPENAI_API_KEY")
# LLM Prompt for Feedback Summary
def generate_feedback_summary(feedback_list):
    prompt = (
        "Here is a collection of feedback from a user's sales conversation:\n\n"
        + "\n".join(f"- {f['short_feedback']}: {f['long_feedback']}" for f in feedback_list)
        + """\n\nBased on this, provide:\n
        1. **Three positive tips** that highlight what the user is doing well.(5-7 words each)\n
        2. **Three improvement tips** that suggest specific areas to enhance performance.(5-7 words each)\n\n
        **Format the response as JSON**, ensuring the points are concise and actionable.
        JSON format:
        {
        "summary" : {
            "positive_tips" : ["tip_1" , "tip_2", "tip_3"] ,
            "improvement_tips" : ["tip_1" , "tip_2", "tip_3"]
        }
    }
        """
    )

    response = openai.ChatCompletion.create(
        model="gpt-4",  # Use GPT-4 or another LLM
        messages=[{"role": "system", "content": "You are an AI assistant skilled in analyzing sales feedback."},
                  {"role": "user", "content": prompt}],
        temperature=0.7,
    )

    return response["choices"][0]["message"]["content"]


@app.get("/feedback_summary/")
async def get_feedback_summary(user_id: str):
    try:
        feedback_ref = db.collection("feedback")

        # Fetch all feedback for the user_id
        query = feedback_ref.where("user_id", "==", user_id)
        results = [doc.to_dict() for doc in query.stream()]

        if not results:
            raise HTTPException(status_code=404, detail="No feedback found for the given user_id")

        # Sort results by timestamp in descending order and get the 5 most recent entries
        sorted_results = sorted(results, key=lambda x: x.get('timestamp', 0), reverse=True)[:5]

        # Collect feedback data from the 5 most recent entries
        all_feedback = []
        for feedback_entry in sorted_results:
            if "feedback" in feedback_entry:
                all_feedback.extend(feedback_entry["feedback"])

        if not all_feedback:
            raise HTTPException(status_code=404, detail="No valid feedback found for the given user_id")

        # Generate summary using LLM
        llm_response = generate_feedback_summary(all_feedback)
        llm_response = json.loads(llm_response)
        return {"summary": llm_response}

    except GoogleAPICallError as e:
        raise HTTPException(status_code=500, detail=f"Firestore Error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating summary: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


