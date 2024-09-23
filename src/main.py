from azure.communication.callautomation import CallAutomationClient
from azure.communication.callautomation.models import CallInvite, CommunicationIdentifier
import os

connection_string = os.getenv("AZURE_CONNECTION_STRING")
call_client = CallAutomationClient.from_connection_string(connection_string)

# Example of handling an incoming call
def handle_incoming_call(call_data):
    call_connection = call_client.create_call_connection(
        CallInvite(
            target_participant=CommunicationIdentifier(phone_number=call_data['from']),
            callback_uri="https://your_server.com/callback"
        )
    )
    # Call is connected, you can now handle voice
    return call_connection.call_connection_id


import azure.cognitiveservices.speech as speechsdk

def recognize_speech_from_audio(audio_stream):
    AZURE_SPEECH_KEY = os.getenv(AZURE_SPEECH_KEY)
    speech_config = speechsdk.SpeechConfig(subscription=AZURE_SPEECH_KEY, region="Your_Region")
    audio_config = speechsdk.audio.AudioConfig(stream=audio_stream)

    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
    result = speech_recognizer.recognize_once()

    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        return result.text
    else:
        return "Error recognizing speech."


import openai

openai.api_key = "your_openai_api_key"

def get_openai_response(user_text):
    response = openai.Completion.create(
        model="gpt-4",
        prompt=user_text,
        max_tokens=100,
        temperature=0.7
    )
    return response.choices[0].text.strip()


def convert_text_to_speech(response_text):
    speech_config = speechsdk.SpeechConfig(subscription="Your_Azure_Speech_Key", region="Your_Region")
    audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)

    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    speech_synthesizer.speak_text_async(response_text).get()



def handle_call_audio(audio_stream):
    # Step 1: Convert caller's speech to text
    user_text = recognize_speech_from_audio(audio_stream)

    # Step 2: Get response from OpenAI
    openai_response = get_openai_response(user_text)

    # Step 3: Convert OpenAI response to speech
    convert_text_to_speech(openai_response)
