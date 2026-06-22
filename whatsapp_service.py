import os
import requests

def get_whatsapp_config():
    access_token = os.environ.get("WHATSAPP_ACCESS_TOKEN")
    phone_number_id = os.environ.get("WHATSAPP_PHONE_NUMBER_ID")
    if not access_token or not phone_number_id:
        return None, None
    return access_token, phone_number_id

def send_whatsapp_message(to_number, message_text):
    access_token, phone_number_id = get_whatsapp_config()
    if not access_token or not phone_number_id:
        return {"error": "WhatsApp Business API not fully configured (missing token or phone number ID)"}

    url = f"https://graph.facebook.com/v17.0/{phone_number_id}/messages"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to_number,
        "type": "text",
        "text": {"body": message_text}
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def send_whatsapp_template(to_number, template_name, language_code="en_US"):
    access_token, phone_number_id = get_whatsapp_config()
    if not access_token or not phone_number_id:
        return {"error": "WhatsApp Business API not fully configured (missing token or phone number ID)"}

    url = f"https://graph.facebook.com/v17.0/{phone_number_id}/messages"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to_number,
        "type": "template",
        "template": {
            "name": template_name,
            "language": {"code": language_code}
        }
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}
