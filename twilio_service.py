import os
from twilio.rest import Client

def get_twilio_config():
    account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
    auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
    from_number = os.environ.get('TWILIO_FROM_NUMBER')
    if not all([account_sid, auth_token, from_number]):
        return None, None, None
    return account_sid, auth_token, from_number

def send_sms(to_number, message_body):
    """
    Sends an SMS via Twilio.
    """
    account_sid, auth_token, from_number = get_twilio_config()
    if not account_sid:
        return {"error": "Twilio credentials not configured"}

    try:
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            body=message_body,
            from_=from_number,
            to=to_number
        )
        return {"status": "success", "sid": message.sid}
    except Exception as e:
        return {"error": str(e)}

def send_whatsapp(to_number, message_body):
    """
    Sends a WhatsApp message via Twilio.
    """
    account_sid, auth_token, from_number = get_twilio_config()
    if not account_sid:
        return {"error": "Twilio credentials not configured"}

    try:
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            body=message_body,
            from_=f"whatsapp:{from_number}",
            to=f"whatsapp:{to_number}"
        )
        return {"status": "success", "sid": message.sid}
    except Exception as e:
        return {"error": str(e)}
