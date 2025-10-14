# app/api/v1/upload.py
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from sqlalchemy.orm import Session
from ...database import get_db
from ...core.cloudinary import upload_image
from ...crud.property import add_property_image, get_property
from ...dependencies import get_current_active_user
from ...models.user import User

router = APIRouter(prefix="/upload", tags=["Upload"])

@router.post("/property/{property_id}/image")
async def upload_property_image(
    property_id: int,
    file: UploadFile = File(...),
    caption: str = None,
    order: int = 0,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Upload image for a property"""
    # Verify property exists
    property = get_property(db, property_id)
    if not property:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Property not found"
        )
    
    # Validate file type
    if not file.content_type.startswith('image/'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be an image"
        )
    
    # Upload to Cloudinary
    contents = await file.read()
    result = upload_image(contents, folder=f"tirupur-homes/property-{property_id}")
    
    # Save to database
    db_image = add_property_image(
        db=db,
        property_id=property_id,
        url=result["url"],
        public_id=result["public_id"],
        caption=caption,
        order=order
    )
    
    return {
        "id": db_image.id,
        "url": db_image.url,
        "public_id": db_image.public_id,
        "message": "Image uploaded successfully"
    }