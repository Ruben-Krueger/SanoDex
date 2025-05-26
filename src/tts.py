import pyttsx3

class TTS:
    def __init__(self):
        # Initialize the text-to-speech engine
        self.engine = pyttsx3.init()
        
        # Set properties (optional)
        self.engine.setProperty('rate', 150)    # Speed of speech
        self.engine.setProperty('volume', 1.0)  # Volume (0.0 to 1.0)

    def say(self, message):
        print(message)
        
        # Convert text to speech and play it
        self.engine.say(message)
        self.engine.runAndWait()