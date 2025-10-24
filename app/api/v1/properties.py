# app/api/v1/properties.py
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ...database import get_db
from ...schemas.property import (
    PropertyCreate,
    PropertyUpdate,
    PropertyResponse,
    PropertyListResponse,
    PropertyType,
    PropertyStatus
)
from ...crud import property as crud_property
from ...dependencies import get_current_active_user, get_current_admin_user
from ...models.user import User

router = APIRouter(prefix="/properties", tags=["Properties"])

@router.get("/", response_model=List[PropertyListResponse])
def list_properties(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    property_type: Optional[PropertyType] = None,
    min_price: Optional[float] = Query(None, ge=0),
    max_price: Optional[float] = Query(None, ge=0),
    min_bedrooms: Optional[int] = Query(None, ge=1),
    city: Optional[str] = None,
    search: Optional[str] = None,
    is_featured: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """Get list of properties with filters"""
    properties = crud_property.get_properties(
        db=db,
        skip=skip,
        limit=limit,
        property_type=property_type,
        min_price=min_price,
        max_price=max_price,
        min_bedrooms=min_bedrooms,
        city=city,
        search=search,
        is_featured=is_featured
    )
    
    # Add thumbnail to each property
    result = []
    for prop in properties:
        prop_dict = PropertyListResponse.model_validate(prop).model_dump()
        if prop.images:
            prop_dict['thumbnail'] = prop.images[0].url
        result.append(PropertyListResponse(**prop_dict))
    
    return result

@router.get("/{property_id}", response_model=PropertyResponse)
def get_property(property_id: int, db: Session = Depends(get_db)):
    """Get single property by ID"""
    db_property = crud_property.get_property(db, property_id)
    if not db_property:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Property not found"
        )
    return db_property

@router.get("/slug/{slug}", response_model=PropertyResponse)
def get_property_by_slug(slug: str, db: Session = Depends(get_db)):
    """Get single property by slug"""
    db_property = crud_property.get_property_by_slug(db, slug)
    if not db_property:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Property not found"
        )
    return db_property

@router.post("/", response_model=PropertyResponse, status_code=status.HTTP_201_CREATED)
def create_property(
    property: PropertyCreate,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Create new property (Admin only)"""
    return crud_property.create_property(db=db, property=property, user_id=current_user.id)

@router.put("/{property_id}", response_model=PropertyResponse)
def update_property(
    property_id: int,
    property: PropertyUpdate,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Update property (Admin only)"""
    db_property = crud_property.update_property(db, property_id, property)
    if not db_property:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Property not found"
        )
    return db_property

@router.delete("/{property_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_property(
    property_id: int,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Delete property (Admin only)"""
    success = crud_property.delete_property(db, property_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Property not found"
        )
    return None


# #### MOCK ####

# # app/api/v1/properties.py (With mock data)
# from fastapi import APIRouter, Query, HTTPException, status
# from typing import List, Optional
# from ...schemas.property import PropertyListResponse, PropertyResponse, PropertyType

# router = APIRouter(prefix="/properties", tags=["Properties"])

# # Mock data for testing
# MOCK_PROPERTIES = [
#     {
#         "id": 1,
#         "title": "Luxury 3 BHK Apartment",
#         "slug": "luxury-3-bhk-apartment",
#         "price": 5500000,
#         "property_type": "BUY",
#         "status": "AVAILABLE",
#         "city": "Tirupur",
#         "bedrooms": 3,
#         "bathrooms": 2,
#         "area": 1500,
#         "is_featured": True,
#         "thumbnail": "https://via.placeholder.com/400x300",
#         "created_at": "2024-01-15T10:30:00",
#         "description": "Beautiful luxury apartment with modern amenities",
#         "address": "123 MG Road",
#         "state": "Tamil Nadu",
#         "zip_code": "641601",
#         "parking": True,
#         "furnished": True,
#         "images": [
#             {"id": 1, "url": "https://via.placeholder.com/800x600", "order": 0}
#         ]
#     },
#     {
#         "id": 2,
#         "title": "2 BHK Apartment for Rent",
#         "slug": "2-bhk-apartment-rent",
#         "price": 15000,
#         "property_type": "RENT",
#         "status": "AVAILABLE",
#         "city": "Tirupur",
#         "bedrooms": 2,
#         "bathrooms": 1,
#         "area": 950,
#         "is_featured": False,
#         "thumbnail": "https://via.placeholder.com/400x300",
#         "created_at": "2024-01-14T09:20:00",
#         "description": "Comfortable 2BHK apartment in prime location",
#         "address": "456 Railway Road",
#         "state": "Tamil Nadu",
#         "zip_code": "641602",
#         "parking": True,
#         "furnished": False,
#         "images": [
#             {"id": 2, "url": "https://via.placeholder.com/800x600", "order": 0}
#         ]
#     },
#     {
#         "id": 3,
#         "title": "Independent House for Sale",
#         "slug": "independent-house-sale",
#         "price": 8500000,
#         "property_type": "SELL",
#         "status": "AVAILABLE",
#         "city": "Tirupur",
#         "bedrooms": 4,
#         "bathrooms": 3,
#         "area": 2200,
#         "is_featured": True,
#         "thumbnail": "https://via.placeholder.com/400x300",
#         "created_at": "2024-01-13T14:45:00",
#         "description": "Spacious independent house with garden",
#         "address": "789 Kumaran Road",
#         "state": "Tamil Nadu",
#         "zip_code": "641603",
#         "parking": True,
#         "furnished": False,
#         "images": [
#             {"id": 3, "url": "https://via.placeholder.com/800x600", "order": 0}
#         ]
#     },
# ]

# @router.get("/", response_model=List[PropertyListResponse])
# def list_properties(
#     skip: int = Query(0, ge=0),
#     limit: int = Query(20, ge=1, le=100),
#     property_type: Optional[PropertyType] = None,
#     min_price: Optional[float] = Query(None, ge=0),
#     max_price: Optional[float] = Query(None, ge=0),
#     min_bedrooms: Optional[int] = Query(None, ge=1),
#     city: Optional[str] = None,
#     search: Optional[str] = None,
#     is_featured: Optional[bool] = None,
# ):
#     """Get list of properties with filters (MOCK DATA)"""
    
#     # Filter mock data
#     filtered = MOCK_PROPERTIES.copy()
    
#     if property_type:
#         filtered = [p for p in filtered if p["property_type"] == property_type.value]
    
#     if min_price:
#         filtered = [p for p in filtered if p["price"] >= min_price]
    
#     if max_price:
#         filtered = [p for p in filtered if p["price"] <= max_price]
    
#     if min_bedrooms:
#         filtered = [p for p in filtered if p["bedrooms"] >= min_bedrooms]
    
#     if city:
#         filtered = [p for p in filtered if city.lower() in p["city"].lower()]
    
#     if is_featured is not None:
#         filtered = [p for p in filtered if p["is_featured"] == is_featured]
    
#     if search:
#         filtered = [
#             p for p in filtered 
#             if search.lower() in p["title"].lower() or 
#                search.lower() in p["description"].lower()
#         ]
    
#     # Pagination
#     return filtered[skip:skip + limit]

# @router.get("/{property_id}", response_model=PropertyResponse)
# def get_property(property_id: int):
#     """Get single property by ID (MOCK DATA)"""
#     property = next((p for p in MOCK_PROPERTIES if p["id"] == property_id), None)
    
#     if not property:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Property not found"
#         )
    
#     return property

# @router.get("/slug/{slug}", response_model=PropertyResponse)
# def get_property_by_slug(slug: str):
#     """Get single property by slug (MOCK DATA)"""
#     property = next((p for p in MOCK_PROPERTIES if p["slug"] == slug), None)
    
#     if not property:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Property not found"
#         )
    
#     return property

# # For testing POST/PUT/DELETE without auth
# @router.post("/", status_code=status.HTTP_201_CREATED)
# def create_property_mock(property: dict):
#     """Create property (MOCK - returns dummy response)"""
#     new_property = property.copy()
#     new_property["id"] = len(MOCK_PROPERTIES) + 1
#     new_property["slug"] = property.get("title", "").lower().replace(" ", "-")
#     new_property["created_at"] = "2024-01-15T10:30:00"
#     return new_property

# @router.put("/{property_id}")
# def update_property_mock(property_id: int, property: dict):
#     """Update property (MOCK - returns dummy response)"""
#     return {"message": "Property updated", "id": property_id, **property}

# @router.delete("/{property_id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_property_mock(property_id: int):
#     """Delete property (MOCK)"""
#     return None