
from twilio.twiml.voice_response import VoiceResponse
import logging
from services.acs_client import ACSClient
from services.stt_service import SpeechToTextService
from services.tts_service import TextToSpeechService
from services.openai_service import OpenAIService
from twilio.rest import Client

from datetime import datetime


# Initialize services
acs_client = ACSClient(Settings.ACS_CONNECTION_STRING)
stt_service = SpeechToTextService(Settings.AZURE_SPEECH_KEY, Settings.AZURE_REGION)
tts_service = TextToSpeechService(Settings.AZURE_SPEECH_KEY, Settings.AZURE_REGION)
openai_service = OpenAIService(Settings.OPENAI_API_KEY)
twilio_client = Client(Settings.TWILIO_ACCOUNT_SID, Settings.TWILIO_AUTH_TOKEN)

required_fields = ["name", "dob", "referral", "physician", "chief_complaint", "address", "phone", "date", "time"]

class Agent:

    def __init__(self):
        self.response = VoiceResponse()
        self.stage = 0
        self.user_data = {}

        self.start_time = None
        self.end_time = None

    def has_required_data(self):
        return all(field in self.user_data for field in required_fields)

    def initiate_conversation(self):
        self.start_time = datetime.now()
        self.response.say("Hello, thank you for calling SanoDex. I'm an artificial intelligence system to make scheduling your appointment easy")

    def is_conversation_active():
        return self.start_time and not self.end_time

    def send_email(self):
        # TODO: send email
        self.response.say("I've sent you an email with these details")

    def end_conversation(self):
        self.send_email()
        self.end_time = datetime.now()

    def extract_information(self, user_input):
        # Instruct ChatGPT to handle complex cases and extract data intelligently
        prompt = f"""
        A caller is providing information about themselves. Extract their name and date of birth if provided:
        - If the caller says their name, capture it as 'name'.
        - If the caller mentions their date of birth, capture it as 'dob'.
        Example input: 'My name is John Doe and I was born on March 3, 1995'
        Expected output: name='John Doe', dob='March 3, 1995'
        
        Input: '{user_input}'
        """
        try:
            response = openai_service.get_openai_response(prompt)
            return response
        except Exception as error:
            logging.exception(error)
            return "An unexpected error occurred"

    def handle_conversation(self):
        # Get audio from the Twilio request (You will need Twilio Media Streams for real-time audio)
        audio_url = request.form.get('RecordingUrl')

        if audio_url:
            # Use the STT service to convert speech to text from Twilio Recording URL
            user_text = stt_service.recognize_speech_from_audio(audio_url)

            # Get response from OpenAI
            ai_response = openai_service.get_openai_response(user_text)
            
            # Convert AI response to speech and play it back to the caller
            response.say(ai_response)
        else:
            response.say("Sorry, we could not process your request.")

        return str(response)
