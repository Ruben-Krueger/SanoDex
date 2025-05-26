import websocket
import logging
import pyaudio
import tkinter as tk
from tkinter import ttk
import threading
from tts import TTS

# Audio settings for Vosk (must match server settings)
CHUNK = 1536  # Match the chunk size used by Vosk
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000  # Must be 16kHz for Vosk


class Client:
    def __init__(self):
        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.ws = None
        self.is_streaming = False
        self.stream = None
        self.audio = None

        self.tts = TTS()

    def start(self):
        logging.info("Starting WebSocket client")
        self.ws = websocket.WebSocketApp(
            "ws://0.0.0.0:8765",
            on_open=self.on_open,
            on_message=self.on_message,
            on_close=self.on_close,    
            on_error=self.on_error
        )
        # Run WebSocket connection in a separate thread
        self.ws_thread = threading.Thread(target=self.ws.run_forever)
        self.ws_thread.daemon = True
        self.ws_thread.start()

    def on_open(self, ws):
        logging.info("WebSocket connection established")
        self.start_streaming()

    def start_streaming(self):
        logging.info("Starting audio stream...")
        try:
            self.is_streaming = True
            self.audio = pyaudio.PyAudio()
            self.stream = self.audio.open(
                format=FORMAT, 
                channels=CHANNELS, 
                rate=RATE, 
                input=True, 
                frames_per_buffer=CHUNK
            )

            # Run audio streaming in a separate thread
            self.stream_thread = threading.Thread(target=self.stream_audio)
            self.stream_thread.daemon = True
            self.stream_thread.start()

        except Exception as e:
            logging.error(f"Error starting audio stream: {e}")
            self.stop_streaming()

    def stream_audio(self):
        try:
            while self.is_streaming and self.ws and self.ws.sock and self.ws.sock.connected:
                data = self.stream.read(CHUNK, exception_on_overflow=False)
                if data and self.ws and self.ws.sock and self.ws.sock.connected:
                    self.ws.send(data, opcode=websocket.ABNF.OPCODE_BINARY)
        except Exception as e:
            logging.error(f"Error in audio streaming: {e}")
        finally:
            self.stop_streaming()

    def stop_streaming(self):
        logging.info("Stopping stream...")
        self.is_streaming = False
        
        if self.stream:
            try:
                self.stream.stop_stream()
                self.stream.close()
            except Exception as e:
                logging.error(f"Error closing audio stream: {e}")
            self.stream = None

        if self.audio:
            try:
                self.audio.terminate()
            except Exception as e:
                logging.error(f"Error terminating audio: {e}")
            self.audio = None

        if self.ws:
            try:
                self.ws.close()
            except Exception as e:
                logging.error(f"Error closing WebSocket: {e}")
            self.ws = None

    def on_message(self, ws, message):
        logging.info(f"Received: {message}")
        self.tts.say(message)

    def on_close(self, ws, close_status_code, close_msg):
        logging.info(f"Connection closed (status code: {close_status_code}, message: {close_msg})")
        self.stop_streaming()

    def on_error(self, ws, error):
        logging.error(f"WebSocket error: {error}")
        self.stop_streaming()


class ClientUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("SanoDex")
        self.root.geometry("800x600")  # Set window size
        
        # Create main frame
        self.main_frame = ttk.Frame(self.root, padding="20")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create and style the call button
        self.call_button = tk.Button(
            self.main_frame,
            text="Call 📞",
            command=self.handle_call,
            bg='#008000',  # Nice green color
            fg='white',
            padx=20,
            pady=10,
            relief=tk.RAISED,
        )
        self.call_button.grid(row=0, column=0, pady=20)
        
        # Center the button
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        self.client = Client()

    def handle_call(self):
        self.client.start()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":    
    app = ClientUI()
    app.run()
