import asyncio
import websockets
import logging
import os
from stt import STT
import json
from agent import Agent
# Configuration
HOST = os.getenv('WEBSOCKET_HOST', '0.0.0.0')  # Accept connections from any IP
PORT = int(os.getenv('WEBSOCKET_PORT', 8765))
SSL_CERT = os.getenv('SSL_CERT_PATH') 
SSL_KEY = os.getenv('SSL_KEY_PATH')

STT_MODEL_PATH = os.getenv('STT_MODEL_PATH')

async def handle_audio(websocket, path):
    client_address = websocket.remote_address
    logging.info(f"New connection from {client_address}")

    agent = Agent()

    try:
        with STT(STT_MODEL_PATH) as stt:
            async for message in websocket:
                # Process the incoming audio data through STT
                if stt.recognizer.AcceptWaveform(message):
                    result = json.loads(stt.recognizer.Result())
                    text = result["text"].strip()
                    if text:
                        logging.info(f"Transcribed text from {client_address}: '{text}'")
                        response = agent.handle_message(text)
                        await websocket.send(response)
                        logging.info(f"Sent response to {client_address}: '{response}'")

    except websockets.exceptions.ConnectionClosed:
        logging.info(f"Client {client_address} disconnected")
    except Exception as e:
        logging.error(f"Error handling client {client_address}: {str(e)}")

if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    logging.info(f"Starting WebSocket server on {HOST}:{PORT}")

    # SSL context for secure WebSocket (WSS)
    ssl_context = None
    if SSL_CERT and SSL_KEY:
        import ssl
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        ssl_context.load_cert_chain(SSL_CERT, SSL_KEY)
        logging.info("SSL enabled - using secure WebSocket (WSS)")

    # Start the WebSocket server
    start_server = websockets.serve(
        handle_audio, 
        HOST, 
        PORT,
        ssl=ssl_context
    )

    # Run the server
    asyncio.get_event_loop().run_until_complete(start_server)
    logging.info("Server is running...")
    asyncio.get_event_loop().run_forever()

