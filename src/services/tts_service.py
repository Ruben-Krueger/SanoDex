import azure.cognitiveservices.speech as speechsdk

class TextToSpeechService:
    def __init__(self, subscription_key, region):
        self.speech_config = speechsdk.SpeechConfig(subscription=subscription_key, region=region)

    def convert_text_to_speech(self, response_text):
        audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
        speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=self.speech_config, audio_config=audio_config)
        speech_synthesizer.speak_text_async(response_text).get()
