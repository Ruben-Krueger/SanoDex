import websocket
import logging
import pyaudio
import tkinter as tk
from tkinter import ttk

# Number of frames per buffer (1024 frames = 2048 bytes at 16-bit = 64ms at 16kHz)
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000


class Client:

    def __init__(self):
         # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.ws = None

    def start(self):
        logging.info("Starting WebSocket client")
        self.ws = websocket.WebSocketApp(
            "ws://0.0.0.0:8765",
            on_open=self.on_open,
            on_message=self.on_message,
            on_close=self.on_close,    
            on_error=self.on_error
        )
        self.ws.run_forever()


    def on_open(self, ws):
        print("Streaming mic input...")
        p = pyaudio.PyAudio()
        stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

        try:
            while True:
                data = stream.read(CHUNK)
                logging.info("Read chunk of audio")
                ws.send(data, opcode=websocket.ABNF.OPCODE_BINARY)
                logging.info("Sent chunk of audio")
        except KeyboardInterrupt:
            logging.info("Stopping...")
            stream.stop_stream()
            stream.close()
            p.terminate()
            ws.close()

        except Exception as e:
            logging.error(f"Error: {e}")
            stream.stop_stream()
            stream.close()
            p.terminate()
            ws.close()


    def on_message(self, ws, message):
        logging.info(f"Received: {message}")


    def on_close(self, ws, close_status_code, close_msg):
        logging.info("Connection closed")

    def on_error(self, ws, error):
        logging.error(f"Error: {error}")


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
        # This will be implemented later to handle the call functionality
        print("Call button pressed")

        self.client.start()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":    
    app = ClientUI()
    app.run()
