import os
import requests

def get_tiktok_config():
    access_token = os.environ.get("TIKTOK_ACCESS_TOKEN")
    if not access_token:
        return None
    return access_token

def get_tiktok_user_info():
    access_token = get_tiktok_config()
    if not access_token:
        return {"error": "TikTok API not configured"}

    url = "https://open-api.tiktok.com/user/info/"
    params = {
        "access_token": access_token
    }

    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def share_to_tiktok(video_url, text):
    """
    Simulates sharing a video to TikTok using the TikTok Content Posting API.
    """
    access_token = get_tiktok_config()
    if not access_token:
        return {"error": "TikTok API not configured"}

    # In a real integration, this would use the direct video upload or share-to-TikTok flow
    # Ref: https://developers.tiktok.com/doc/content-posting-api-reference-post-video
    url = "https://open.tiktokapis.com/v2/post/publish/video/init/"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json; charset=UTF-8"
    }
    payload = {
        "source": "PULL_FROM_URL",
        "video_url": video_url,
        "post_info": {
            "title": text,
            "privacy_level": "PUBLIC_TO_EVERYONE",
            "disable_comment": False,
            "disable_duet": False,
            "disable_stitch": False,
            "video_label_from_creator": "UNSPECIFIED"
        }
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        # We handle 200 as success, even if it's a mock response from a dev environment
        if response.status_code == 200:
            return response.json()
        return {"status": "error", "message": f"TikTok API error: {response.text}", "code": response.status_code}
    except Exception as e:
        return {"error": str(e)}
