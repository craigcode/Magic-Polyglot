import os
from twilio.rest import Client


def send_sms(recipient,text):
    client = Client(os.environ.get('TWILIO_ACCOUNT_SID'), 
                os.environ.get('TWILIO_AUTH_TOKEN'))

    message = client.messages.create(
    from_=os.environ.get('TWILIO_NUMBER'),
    body=text,
    to=recipient
    )

    print(message.sid)