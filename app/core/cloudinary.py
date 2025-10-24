# app/core/cloudinary.py
import cloudinary
import cloudinary.uploader
from ..config import settings

cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET
)

def upload_image(file_data, folder="tirupur-homes"):
    """Upload image to Cloudinary"""
    result = cloudinary.uploader.upload(
        file_data,
        folder=folder,
        resource_type="auto"
    )
    return {
        "url": result["secure_url"],
        "public_id": result["public_id"]
    }

def delete_image(public_id: str):
    """Delete image from Cloudinary"""
    return cloudinary.uploader.destroy(public_id)