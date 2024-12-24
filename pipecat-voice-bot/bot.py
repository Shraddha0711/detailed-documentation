import os
import re
import sys
import json
import base64
import wave
import argparse
import asyncio
from typing import Dict
from urllib.parse import urlparse
import firebase_admin
from firebase_admin import firestore, credentials
from dotenv import load_dotenv
from loguru import logger
from pipecat.audio.vad.silero import SileroVADAnalyzer
from pipecat.frames.frames import EndFrame, LLMMessagesFrame
from pipecat.pipeline.pipeline import Pipeline
from pipecat.pipeline.runner import PipelineRunner
from pipecat.pipeline.task import PipelineParams, PipelineTask
from pipecat.processors.aggregators.openai_llm_context import OpenAILLMContext
from pipecat.processors.audio.audio_buffer_processor import AudioBufferProcessor
from pipecat.services.elevenlabs import ElevenLabsTTSService
from pipecat.services.cartesia import CartesiaTTSService
from pipecat.services.openai import OpenAILLMService
from pipecat.transports.services.daily import DailyParams, DailyTransport, DailyTranscriptionSettings

# Load environment variables from .env file
load_dotenv(override=True)

# Setup logger for debugging and information logging
logger.remove(0)
logger.add(sys.stderr, level="DEBUG")

# Firebase initialization for storing transcription data
FILES_DIR = "saved_files"  # Directory to save audio files
cred = credentials.Certificate(os.getenv("CRED_PATH"))  # Firebase credentials path
firebase_admin.initialize_app(cred)  # Initialize Firebase app
db = firestore.client()  # Firestore client for database interactions

# Function to save transcription data into Firebase
async def save_in_db(room_id: str, transcript: str):
    """
    Saves the transcription data to Firebase Firestore under the 'Transcription' collection.
    The room ID and prompt type are also extracted from the transcript for storage.
    """
    doc_ref = db.collection("Transcription").document(room_id)
    # Extracting the prompt type from the system message
    prompt_type = next((msg['content'].split(':')[-1].strip() for msg in transcript if msg.get('role') == 'system' and 'prompt_type' in msg['content']), None)
    # Clean the transcription data
    transcription = re.sub(r'\.?\s*prompt_type:[a-zA-Z]+$', '', transcript[0]['content'])
    data = {"transcript": transcription, "type": prompt_type}
    doc_ref.set(data)
    logger.info(f"Transcription saved successfully for room: {room_id}")

# Function to save audio buffer as a WAV file
async def save_audio(audiobuffer, room_url: str):
    """
    Merges the audio buffers and saves the resulting audio as a WAV file.
    The file is saved in the 'saved_files' directory with a name derived from the room URL.
    """
    if audiobuffer.has_audio():  # Check if the audio buffer contains data
        merged_audio = audiobuffer.merge_audio_buffers()  # Merge all audio buffers
        filename = os.path.join(FILES_DIR, f"audio_{(urlparse(room_url).path).removeprefix('/')}.wav")  # Create filename from room URL
        with wave.open(filename, "wb") as wf:
            wf.setnchannels(2)  # Set number of channels (stereo)
            wf.setsampwidth(2)  # Set sample width (2 bytes)
            wf.setframerate(audiobuffer._sample_rate)  # Set the sample rate of the audio
            wf.writeframes(merged_audio)  # Write the audio data to the file
        logger.info(f"Merged audio saved to {filename}")
    else:
        logger.warning("No audio data to save")  # Log a warning if there's no audio data

# Main execution function for handling room interactions
async def main(room_url: str, token: str, config_b64: str):
    """
    Main function that orchestrates the setup, configuration, and interaction with the daily transport and processing pipeline.
    It manages audio, transcription, and chatbot context flow.
    """
    # Decode and parse the configuration data from base64
    config_str = base64.b64decode(config_b64).decode()  # Decode the base64 config string
    config = json.loads(config_str)  # Convert the decoded string into a dictionary

    # Initialize Daily transport (handles real-time communication and transcription)
    transport = DailyTransport(
        room_url,
        token,
        config['avatar_name'],
        DailyParams(
            audio_out_enabled=True,
            audio_in_enabled=True,
            camera_out_enabled=False,
            vad_enabled=True,  # Voice Activity Detection enabled
            vad_audio_passthrough=True,
            vad_analyzer=SileroVADAnalyzer(),  # Use Silero VAD model for speech detection
            transcription_enabled=True,
            transcription_settings=DailyTranscriptionSettings(language="en", tier="nova", model="2-general")  # Configure transcription settings
        ),
    )

    # Initialize Text-to-Speech (TTS) and Language Model (LLM) services
    tts = ElevenLabsTTSService(api_key=os.getenv("ELEVENLABS_API_KEY"), voice_id=config['voice_id'])  # TTS service for speech synthesis
    llm = OpenAILLMService(api_key=os.getenv("OPENAI_API_KEY"), model="gpt-4o")  # OpenAI LLM service for natural language processing

    # Initial chatbot messages to set up context
    messages = [{"role": "system", "content": config['prompt']}]  # System-level message to configure bot's behavior

    # Initialize context for the OpenAI LLM and aggregator for context updates
    context = OpenAILLMContext(messages)
    context_aggregator = llm.create_context_aggregator(context)
    audiobuffer = AudioBufferProcessor()  # Audio processing buffer for handling audio data

    # Create pipeline of steps that handle data flow: input, processing, output
    pipeline = Pipeline([
        transport.input(),  # Input handler for transport data
        context_aggregator.user(),  # User-side context aggregation
        llm,  # Process input via LLM
        tts,  # Convert text to speech
        transport.output(),  # Output handler for transport data
        audiobuffer,  # Audio buffer processing
        context_aggregator.assistant(),  # Assistant-side context aggregation
    ])

    # Setup and run the pipeline task
    task = PipelineTask(pipeline, PipelineParams(allow_interruptions=True))

    # Event handler when the first participant joins the room
    @transport.event_handler("on_first_participant_joined")
    async def on_first_participant_joined(transport, participant):
        """
        This function is triggered when the first participant joins the room.
        It starts capturing transcription data and queues the initial chatbot messages.
        """
        await transport.capture_participant_transcription(participant["id"])
        await task.queue_frames([LLMMessagesFrame(messages)])  # Send initial system messages
        logger.info(f"First participant joined: {participant['id']}")

    # Event handler when a participant leaves the room
    @transport.event_handler("on_participant_left")
    async def on_participant_left(transport, participant, reason):
        """
        This function is triggered when a participant leaves the room.
        It saves the audio and transcription data and ends the pipeline task.
        """
        participant_id = participant['id']
        logger.info(f"Participant left: {participant_id}")

        # Save the audio and transcription, then finalize the task
        await save_audio(audiobuffer, room_url)
        await save_in_db((urlparse(room_url).path).removeprefix('/'), context.get_messages())  # Save transcription to database
        await task.queue_frame(EndFrame())  # End the pipeline task

    # Run the pipeline task asynchronously
    runner = PipelineRunner()
    await runner.run(task)

# Main entry point for running the script
if __name__ == "__main__":
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description="Pipecat Bot")
    parser.add_argument("-u", required=True, type=str, help="Room URL")  # Room URL to connect to
    parser.add_argument("-t", required=True, type=str, help="Token")  # Access token for authentication
    parser.add_argument("--config", required=True, help="Base64 encoded configuration")  # Base64 encoded configuration
    args = parser.parse_args()

    # Start the main function asynchronously
    asyncio.run(main(args.u, args.t, args.config))
