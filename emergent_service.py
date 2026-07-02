import os
import requests

def get_completion(prompt, model="gpt-4o"):
    """
    Sends a prompt to the Emergent Universal LLM API.
    Note: Emergent provides a Universal Key that gives access to multiple models.
    """
    api_key = os.environ.get("EMERGENT_API_KEY")
    if not api_key:
        return {"error": "EMERGENT_API_KEY not configured"}

    # Base URL for Emergent API
    url = "https://api.emergent.sh/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": model,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post(url, json=payload, timeout=30)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}
