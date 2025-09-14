# outbound_call.py
from twilio.rest import Client
from twilio_setup import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_CALLING_NUMBER

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

def make_outbound_call(to_number):
    call = client.calls.create(
        to=to_number,
        from_=TWILIO_CALLING_NUMBER,
        url="https://your-public-domain.com/outbound_call_handler", 
        record=True  # optional if you want to record
    )
    return call.sid
