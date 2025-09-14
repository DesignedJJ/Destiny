# openai_logic.py

import os
import openai

openai.api_key = os.getenv("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")

SYSTEM_PROMPT = """
You are an AI assistant for a healthcare insurance company. 
You help users with questions about claims and payment status in a polite, concise, and HIPAA-compliant manner. 
You do not provide personal health advice. 
"""

def get_bot_response(conversation_history):
    """
    conversation_history is a list of dictionaries:
    [
      {"role": "system", "content": "..."},
      {"role": "user", "content": "..."},
      {"role": "assistant", "content": "..."},
      ...
    ]

    Returns the next message from the assistant using the OpenAI ChatCompletion API.
    """

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=conversation_history,
        temperature=0.7,
        max_tokens=200
    )

    return response.choices[0].message.content

def initialize_conversation():
    """
    Returns an initial conversation history with the system prompt.
    """
    return [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]
