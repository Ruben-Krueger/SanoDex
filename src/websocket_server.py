import asyncio
import websockets
import logging
import os
from flask_socketio import SocketIO

# Configuration
HOST = os.getenv('WEBSOCKET_HOST', '0.0.0.0')  # Accept connections from any IP
PORT = int(os.getenv('WEBSOCKET_PORT', 8765))
SSL_CERT = os.getenv('SSL_CERT_PATH')  # Path to SSL certificate if using WSS
SSL_KEY = os.getenv('SSL_KEY_PATH')    # Path to SSL key if using WSS

async def handle_audio(websocket, path):
    client_address = websocket.remote_address
    logging.info(f"New connection from {client_address}")
    try:
        async for message in websocket:
            # Handle the streamed audio data here
            # For example, send the audio to a speech-to-text engine
            logging.info(f"Received audio frame from {client_address}")
            await websocket.send("Received audio")
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

