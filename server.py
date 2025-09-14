# server.py
from flask import Flask, request, Response
from twilio.twiml.voice_response import VoiceResponse, Gather
import os
import openai
from openai_logic import get_bot_response, initialize_conversation

app = Flask(__name__)

# In-memory conversation storage (for demo):
# In production, you'd store by session/call SID, e.g. in a database or cache.
conversations = {}

@app.route("/outbound_call_handler", methods=["POST"])
def outbound_call_handler():
    """
    Twilio calls this URL when the outbound call is answered.
    We greet the user and prompt them for input.
    """
    call_sid = request.form.get("CallSid")

    # Initialize conversation if not already
    if call_sid not in conversations:
        conversations[call_sid] = initialize_conversation()

    # Build TwiML to gather speech
    resp = VoiceResponse()
    gather = Gather(
        input="speech",
        speech_timeout="auto",
        action="/process_speech",
        method="POST"
    )
    gather.say("Hello, this is your Healthcare AI Bot. How can I help you today?")
    resp.append(gather)

    return Response(str(resp), mimetype="text/xml")

@app.route("/process_speech", methods=["POST"])
def process_speech():
    """
    Twilio posts speech transcription here if 'input="speech"' was used.
    """
    call_sid = request.form.get("CallSid")
    user_input = request.form.get("SpeechResult")  # The transcribed text

    if not user_input:
        # No speech detected
        resp = VoiceResponse()
        resp.say("I'm sorry, I did not catch that. Goodbye.")
        resp.hangup()
        return Response(str(resp), mimetype="text/xml")

    # Retrieve conversation from memory
    conversation = conversations.get(call_sid)
    if not conversation:
        conversation = initialize_conversation()
        conversations[call_sid] = conversation

    # Append the user's message
    conversation.append({"role": "user", "content": user_input})

    # Get AI response from OpenAI
    ai_response = get_bot_response(conversation)

    # Append AI response back to the conversation
    conversation.append({"role": "assistant", "content": ai_response})

    # Next TwiML to speak AI's response, then gather more
    resp = VoiceResponse()
    gather = Gather(
        input="speech",
        speech_timeout="auto",
        action="/process_speech",
        method="POST"
    )
    gather.say(ai_response)
    resp.append(gather)

    return Response(str(resp), mimetype="text/xml")


if __name__ == "__main__":
    # For local dev, run on a port and use ngrok or similar to expose it publicly
    app.run(debug=True, port=5000)
