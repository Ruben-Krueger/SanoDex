from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    ACS_CONNECTION_STRING = os.getenv("ACS_CONNECTION_STRING")
    AZURE_SPEECH_KEY = os.getenv("AZURE_SPEECH_KEY")
    AZURE_REGION = os.getenv("AZURE_REGION")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
    TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")

    MAX_CONVERSATION_LENGTH_SECONDS = 600 # 10 minutes

