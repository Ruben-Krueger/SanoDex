from flask import Flask, request, Response
from config.settings import Settings
import os
import logging
from agent import Agent

app = Flask(__name__)


@app.route("/twilio/webhook", methods=['POST'])
def handle_incoming_call():
    """Handles incoming call from Twilio and routes to Azure and OpenAI services."""
    call_sid = request.form.get('CallSid')
    from_number = request.form.get('From')
    logging.info(f"Recieving call from {from_number}")

    agent = Agent()
    agent.initiate_conversation()

    while agent.is_conversation_active():
        agent.handle_conversation()

if __name__ == "__main__":
    app.run(debug=True)
