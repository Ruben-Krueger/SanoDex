import asyncio
import websockets
import logging
from flask_socketio import SocketIO

async def handle_audio(websocket, path):
    logging.info("Handling audio")
    async for message in websocket:
        # Handle the streamed audio data here
        # For example, send the audio to a speech-to-text engine
        print("Received audio frame:", message)

        await websocket.send("Received audio")

# Start the WebSocket server
start_server = websockets.serve(handle_audio, "localhost", 8765)  # Adjust the address as needed

# Run the server
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

