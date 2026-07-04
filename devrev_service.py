import os
import requests

DEVREV_API_BASE = "https://api.devrev.ai"

def get_headers():
    token = os.environ.get("DEVREV_TOKEN")
    if not token:
        return None
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

def create_work(title, body, work_type="ticket", applies_to_part=None):
    """
    Creates a new work item (issue, ticket, task, or opportunity) in DevRev.
    """
    headers = get_headers()
    if not headers:
        return {"error": "DevRev token not configured"}

    url = f"{DEVREV_API_BASE}/works.create"
    payload = {
        "type": work_type,
        "title": title,
        "body": body
    }

    if applies_to_part:
        payload["applies_to_part"] = applies_to_part
    else:
        # Default part if not provided
        default_part = os.environ.get("DEVREV_DEFAULT_PART_ID")
        if default_part:
            payload["applies_to_part"] = default_part

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        if response.status_code >= 400:
            return {"error": f"DevRev API Error {response.status_code}: {response.text}"}
        return {"status": "success", "work": response.json()}
    except Exception as e:
        return {"error": str(e)}

def get_self():
    """
    Retrieves information about the authenticated user.
    """
    headers = get_headers()
    if not headers:
        return {"error": "DevRev token not configured"}

    url = f"{DEVREV_API_BASE}/dev-users.self"
    try:
        response = requests.get(url, headers=headers, timeout=30)
        if response.status_code >= 400:
            return {"error": f"DevRev API Error {response.status_code}: {response.text}"}
        return {"status": "success", "user": response.json()}
    except Exception as e:
        return {"error": str(e)}
