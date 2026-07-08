import os
import requests
import base64

def get_auth_header():
    email = os.environ.get("ZENDESK_EMAIL")
    token = os.environ.get("ZENDESK_TOKEN")
    if not email or not token:
        return None

    # Zendesk uses email/token:token format for API token authentication
    auth_str = f"{email}/token:{token}"
    encoded_auth = base64.b64encode(auth_str.encode('ascii')).decode('ascii')
    return {
        "Authorization": f"Basic {encoded_auth}",
        "Content-Type": "application/json"
    }

def get_zendesk_url(path):
    subdomain = os.environ.get("ZENDESK_SUBDOMAIN")
    if not subdomain:
        return None
    return f"https://{subdomain}.zendesk.com/api/v2{path}"

def create_ticket(subject, comment_body, requester_name=None, requester_email=None):
    """
    Creates a new ticket in Zendesk.
    """
    url = get_zendesk_url("/tickets.json")
    headers = get_auth_header()
    if not url or not headers:
        return {"error": "Zendesk configuration missing (email, token, or subdomain)"}

    payload = {
        "ticket": {
            "subject": subject,
            "comment": {
                "body": comment_body
            }
        }
    }

    if requester_name and requester_email:
        payload["ticket"]["requester"] = {
            "name": requester_name,
            "email": requester_email
        }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        if response.status_code >= 400:
            return {"error": f"Zendesk API Error {response.status_code}: {response.text}"}
        return {"status": "success", "ticket": response.json()}
    except Exception as e:
        return {"error": str(e)}

def get_users():
    """
    Retrieves a list of users from Zendesk.
    """
    url = get_zendesk_url("/users.json")
    headers = get_auth_header()
    if not url or not headers:
        return {"error": "Zendesk configuration missing"}

    try:
        response = requests.get(url, headers=headers, timeout=30)
        if response.status_code >= 400:
            return {"error": f"Zendesk API Error {response.status_code}: {response.text}"}
        return {"status": "success", "users": response.json()}
    except Exception as e:
        return {"error": str(e)}
