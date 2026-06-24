import os
from twilio.rest import Client

def get_twilio_client():
    account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
    auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
    if not account_sid or not auth_token:
        return None
    return Client(account_sid, auth_token)

def send_sms(to_number, message_body):
    """
    Sends an SMS using Twilio.
    """
    client = get_twilio_client()
    from_number = os.environ.get('TWILIO_PHONE_NUMBER')
    if not client or not from_number:
        return {"status": "error", "message": "Twilio credentials or phone number not configured"}

    try:
        message = client.messages.create(
            body=message_body,
            from_=from_number,
            to=to_number
        )
        return {"status": "success", "sid": message.sid}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def send_whatsapp_message(to_number, message_body):
    """
    Sends a WhatsApp message using Twilio.
    """
    client = get_twilio_client()
    from_number = os.environ.get('TWILIO_WHATSAPP_NUMBER') # e.g., 'whatsapp:+14155238886'
    if not client or not from_number:
        return {"status": "error", "message": "Twilio credentials or WhatsApp number not configured"}

    if not to_number.startswith('whatsapp:'):
        to_number = f'whatsapp:{to_number}'

    try:
        message = client.messages.create(
            body=message_body,
            from_=from_number,
            to=to_number
        )
        return {"status": "success", "sid": message.sid}
    except Exception as e:
        return {"status": "error", "message": str(e)}
