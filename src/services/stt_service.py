import azure.cognitiveservices.speech as speechsdk
import logging

class SpeechToTextService:
    def __init__(self, subscription_key, region):
        self.speech_config = speechsdk.SpeechConfig(subscription=subscription_key, region=region)

    def recognize_speech_from_audio(self, audio_stream):
        audio_config = speechsdk.audio.AudioConfig(stream=audio_stream)
        speech_recognizer = speechsdk.SpeechRecognizer(speech_config=self.speech_config, audio_config=audio_config)
        result = speech_recognizer.recognize_once()

        if result.reason == speechsdk.ResultReason.RecognizedSpeech:
            return result.text
        else:
            logging.critical("Error recognizing speech") 
            return "Error recognizing speech."
