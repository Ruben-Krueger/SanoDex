
from twilio.twiml.voice_response import VoiceResponse
import logging
from config.settings import Settings
from services.acs_client import ACSClient
from services.stt_service import SpeechToTextService
from services.tts_service import TextToSpeechService
from twilio.rest import Client
import requests
from openai import OpenAI

from datetime import datetime

logging.basicConfig(level = logging.INFO)

# Initialize services
acs_client = ACSClient(Settings.ACS_CONNECTION_STRING)
stt_service = SpeechToTextService(Settings.AZURE_SPEECH_KEY, Settings.AZURE_REGION)
tts_service = TextToSpeechService(Settings.AZURE_SPEECH_KEY, Settings.AZURE_REGION)
openai_service = OpenAI(api_key=Settings.OPENAI_API_KEY,)

twilio_client = Client(Settings.TWILIO_ACCOUNT_SID, Settings.TWILIO_AUTH_TOKEN)

required_fields = ["name", "dob", "referral", "physician", "chief_complaint", "address", "phone", "date", "time"]

class Agent:

    def __init__(self):
        self.response = VoiceResponse()
        self.user_data = {}
        self.stage = 0

        self.start_time = None
        self.end_time = None

    def say(self, text):
        self.response.say(text)
        logging.info(f"SanoDex said: '{text}'")

    def has_required_data(self):
        return all(field in self.user_data for field in required_fields)

    def initiate_conversation(self):
        self.start_time = datetime.now()
        self.say("Hello, thank you for calling SanoDex. I'm an artificial intelligence system to make scheduling your appointment easy.")

    def is_conversation_active():
        return self.start_time and not self.end_time

    def send_email(self):
        try:
            requests.post(
            "https://api.mailgun.net/v3/sandboxac1342976f5b4f45a6640b5b1abc5a84.mailgun.org/messages",
            auth=("api", Settings.MAILGUN_API_KEY),
            data={"from": "SanoDex <mailgun@sandboxac1342976f5b4f45a6640b5b1abc5a84.mailgun.org>",
                "to": ["rubenkrueger99@gmail.com"],
                "subject": "Hello",
                "text": "Here are your appointment details: "})
            self.say("I've sent you an email with these details")
        except error as Exception:
            logging.error(error)
            self.say("I'm sorry, I wasn't able to send an email.")

    def end_conversation(self):
        self.send_email()
        self.end_time = datetime.now()

    def extract_information(self, user_input):
        return self.get_openai_response(f"Extract name and date of birth from this input: '{user_input}'")

    def get_openai_response(self, user_input):
        # Instruct ChatGPT to handle complex cases and extract data intelligently
        prompt = f"""
        You are a helpful AI assistant for a healthcare practice. You must answer the phone for patients trying to schedule appointments. 
        A caller has called and said the following: {user_input}.'
        """
        try:
            response = openai_service.Completion.create(
                model="gpt-4",
                prompt=prompt,
                max_tokens=100,
                temperature=0.7
            )
            return response.choices[0].text.strip()
        except Exception as error:
            logging.exception(error)
            return "An unexpected error occurred"

    def handle_input(self, user_input):
        response = self.get_openai_response(user_input)
        print(response)
        
        if 'name' in extracted_info and 'dob' in extracted_info:
            self.user_data['name'] = extracted_info['name']
            self.user_data['dob'] = extracted_info['dob']
            response = f"Thanks, {self.user_data['name']}. I've noted your date of birth as {self.user_data['dob']}."
            self.stage = 3  # Skip to confirmation
        elif self.stage == 0:
            response = "Hello, welcome to SanoDex. May I know your full name?"
            self.stage += 1
        elif self.stage == 1:
            # Collect name
            self.user_data['name'] = user_input
            response = f"Thanks {user_input}. Can I have your date of birth?"
            self.stage += 1
        elif self.stage == 2:
            # Collect date of birth
            self.user_data['dob'] = user_input
            response = f"Thanks for that. I've noted your name as {self.user_data['name']} and your date of birth as {self.user_data['dob']}"
            self.stage += 1
        elif self.stage == 3:
            response = "Error"
        return response

    def handle_conversation(self):

        while True:
            self.extract_information()

        self.end_conversation()


        # if audio_url:
        #     # Use the STT service to convert speech to text from Twilio Recording URL
        #     user_text = stt_service.recognize_speech_from_audio(audio_url)

        #     # Get response from OpenAI
        #     ai_response = openai_service.get_openai_response(user_text)
            
        #     # Convert AI response to speech and play it back to the caller
        #     response.say(ai_response)
        # else:
        #     response.say("Sorry, we could not process your request.")

        # return str(response)
