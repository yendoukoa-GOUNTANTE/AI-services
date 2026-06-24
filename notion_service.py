import os
import requests

NOTION_TOKEN = os.environ.get('NOTION_TOKEN')
NOTION_BASE_URL = 'https://api.notion.com/v1'

def get_headers():
    return {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }

def create_page(parent_page_id, title, content_blocks=None):
    """
    Creates a new page in Notion.
    """
    if not NOTION_TOKEN:
        return {"error": "Notion Token not configured"}

    url = f"{NOTION_BASE_URL}/pages"
    payload = {
        "parent": {"page_id": parent_page_id},
        "properties": {
            "title": [
                {
                    "text": {"content": title}
                }
            ]
        },
        "children": content_blocks or []
    }

    try:
        response = requests.post(url, json=payload, headers=get_headers(), timeout=15)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {"error": str(e)}

def get_database(database_id):
    """
    Retrieves a Notion database.
    """
    if not NOTION_TOKEN:
        return {"error": "Notion Token not configured"}

    url = f"{NOTION_BASE_URL}/databases/{database_id}"

    try:
        response = requests.get(url, headers=get_headers(), timeout=15)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {"error": str(e)}

def query_database(database_id, filter_params=None):
    """
    Queries a Notion database.
    """
    if not NOTION_TOKEN:
        return {"error": "Notion Token not configured"}

    url = f"{NOTION_BASE_URL}/databases/{database_id}/query"
    payload = filter_params or {}

    try:
        response = requests.post(url, json=payload, headers=get_headers(), timeout=15)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {"error": str(e)}
