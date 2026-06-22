import os
import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url

def init_cloudinary():
    cloud_name = os.environ.get("CLOUDINARY_CLOUD_NAME")
    api_key = os.environ.get("CLOUDINARY_API_KEY")
    api_secret = os.environ.get("CLOUDINARY_API_SECRET")

    if not all([cloud_name, api_key, api_secret]):
        return False

    cloudinary.config(
        cloud_name=cloud_name,
        api_key=api_key,
        api_secret=api_secret,
        secure=True
    )
    return True

def upload_media(file_path, public_id=None):
    if not init_cloudinary():
        return {"error": "Cloudinary not configured"}

    try:
        response = cloudinary.uploader.upload(file_path, public_id=public_id)
        return {"status": "success", "url": response['secure_url'], "public_id": response['public_id']}
    except Exception as e:
        return {"error": str(e)}

def get_optimized_url(public_id, width=500, height=500, crop="fill"):
    if not init_cloudinary():
        return {"error": "Cloudinary not configured"}

    try:
        url, options = cloudinary_url(public_id, width=width, height=height, crop=crop, fetch_format="auto", quality="auto")
        return {"status": "success", "url": url}
    except Exception as e:
        return {"error": str(e)}
