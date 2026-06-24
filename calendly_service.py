import os
import requests

def get_calendly_headers():
    api_key = os.environ.get("CALENDLY_API_KEY")
    if not api_key:
        return None
    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

def get_user_info():
    headers = get_calendly_headers()
    if not headers:
        return {"error": "Calendly API key not configured"}

    try:
        response = requests.get("https://api.calendly.com/users/me", headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def list_event_types(user_uri=None):
    headers = get_calendly_headers()
    if not headers:
        return {"error": "Calendly API key not configured"}

    params = {}
    if user_uri:
        params["user"] = user_uri
    else:
        # If no user_uri, we might need to get it first from /users/me
        user_info = get_user_info()
        if "error" in user_info:
            return user_info
        params["user"] = user_info["resource"]["uri"]

    try:
        response = requests.get("https://api.calendly.com/event_types", headers=headers, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def list_scheduled_events(user_uri=None, count=10):
    headers = get_calendly_headers()
    if not headers:
        return {"error": "Calendly API key not configured"}

    params = {"count": count}
    if user_uri:
        params["user"] = user_uri
    else:
        user_info = get_user_info()
        if "error" in user_info:
            return user_info
        params["user"] = user_info["resource"]["uri"]

    try:
        response = requests.get("https://api.calendly.com/scheduled_events", headers=headers, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
