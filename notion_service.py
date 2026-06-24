import os
from notion_client import Client

NOTION_TOKEN = os.environ.get("NOTION_TOKEN")

def get_notion_client():
    if not NOTION_TOKEN:
        return None
    return Client(auth=NOTION_TOKEN)

def create_page(parent_page_id, title, content_blocks=None):
    """
    Creates a new page in Notion.
    """
    client = get_notion_client()
    if not client:
        return {"error": "Notion token not configured"}

    try:
        new_page = client.pages.create(
            parent={"page_id": parent_page_id},
            properties={
                "title": [
                    {
                        "text": {
                            "content": title
                        }
                    }
                ]
            },
            children=content_blocks or []
        )
        return {"status": "success", "page": new_page}
    except Exception as e:
        return {"error": str(e)}

def add_to_database(database_id, properties):
    """
    Adds a new entry to a Notion database.
    """
    client = get_notion_client()
    if not client:
        return {"error": "Notion token not configured"}

    try:
        new_page = client.pages.create(
            parent={"database_id": database_id},
            properties=properties
        )
        return {"status": "success", "page": new_page}
    except Exception as e:
        return {"error": str(e)}

def get_database(database_id):
    """
    Retrieves a Notion database.
    """
    client = get_notion_client()
    if not client:
        return {"error": "Notion token not configured"}

    try:
        database = client.databases.retrieve(database_id=database_id)
        return {"status": "success", "database": database}
    except Exception as e:
        return {"error": str(e)}

def query_database(database_id, filter_obj=None):
    """
    Queries a Notion database.
    """
    client = get_notion_client()
    if not client:
        return {"error": "Notion token not configured"}

    try:
        results = client.databases.query(database_id=database_id, filter=filter_obj)
        return {"status": "success", "results": results.get("results", [])}
    except Exception as e:
        return {"error": str(e)}
