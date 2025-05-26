import pyaudio
import json
from vosk import Model, KaldiRecognizer

# Load the model - you'll need to download a model from https://alphacephei.com/vosk/models
model = Model("models/vosk-model-en-us-0.22")  # Using the full model for better accuracy
recognizer = KaldiRecognizer(model, 16000)

# Set up audio input
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, 
                channels=1, 
                rate=16000, 
                input=True, 
                frames_per_buffer=3072)  # Increased for better word capture
stream.start_stream()

print("Listening... (Ctrl+C to stop)")

if __name__ == "__main__":
    try:
        while True:
            data = stream.read(1536, exception_on_overflow=False)  # Increased for better word capture
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                print("You said:", result["text"])
            else:
                print("No speech detected")
    except KeyboardInterrupt:
        print("\nStopping...")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()