from flask import Flask, request, Response
from config.settings import Settings
import os
import logging
from agent import Agent
from twilio.twiml.voice_response import VoiceResponse
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

@app.route("/twilio/webhook", methods=['POST'])
def handle_incoming_call():
    # Create a Twilio Voice Response
    response = VoiceResponse()

    # Start streaming audio using the <Stream> TwiML verb
    response.say("Hello, you are now connected. We are streaming your audio.")


    # Manually insert the <Stream> verb
    stream_element = '<Stream url="wss://68b5-24-5-28-13.ngrok-free.app" />'
    response.append(stream_element)


    return str(response)

    # # call_sid = request.form.get('CallSid')
    # # from_number = request.form.get('From')
    # logging.info(f"Recieving call from {from_number}")

    # agent = Agent()
    # agent.initiate_conversation()

    # while agent.is_conversation_active():
    #     agent.handle_conversation()

@socketio.on('message')
def handle_message(data):
    print(f"Received message: {data}")

if __name__ == "__main__":
    app.run(port=8765, debug=True)
