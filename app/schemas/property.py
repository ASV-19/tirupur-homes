# app/schemas/property.py
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime
from ..models.property import PropertyType, PropertyStatus

class PropertyImageBase(BaseModel):
    url: str
    public_id: Optional[str] = None
    caption: Optional[str] = None
    order: int = 0

class PropertyImageCreate(PropertyImageBase):
    pass

class PropertyImageResponse(PropertyImageBase):
    id: int
    uploaded_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class PropertyBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=200)
    description: str
    price: float = Field(..., gt=0)
    property_type: PropertyType
    address: Optional[str] = None
    city: str = "Tirupur"
    state: str = "Tamil Nadu"
    zip_code: Optional[str] = None
    bedrooms: int = Field(default=1, ge=1)
    bathrooms: int = Field(default=1, ge=1)
    area: int = Field(..., gt=0)
    parking: bool = False
    furnished: bool = False
    is_featured: bool = False
    is_special_offer: bool = False
    offer_text: Optional[str] = None

class PropertyCreate(PropertyBase):
    pass

class PropertyUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    property_type: Optional[PropertyType] = None
    status: Optional[PropertyStatus] = None
    address: Optional[str] = None
    city: Optional[str] = None
    bedrooms: Optional[int] = None
    bathrooms: Optional[int] = None
    area: Optional[int] = None
    parking: Optional[bool] = None
    furnished: Optional[bool] = None
    is_featured: Optional[bool] = None

class PropertyResponse(PropertyBase):
    id: int
    slug: str
    status: PropertyStatus
    images: List[PropertyImageResponse] = []
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)

class PropertyListResponse(BaseModel):
    id: int
    title: str
    slug: str
    price: float
    property_type: PropertyType
    status: PropertyStatus
    city: str
    bedrooms: int
    bathrooms: int
    area: int
    is_featured: bool
    thumbnail: Optional[str] = None
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class PropertyFilter(BaseModel):
    property_type: Optional[PropertyType] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    min_bedrooms: Optional[int] = None
    city: Optional[str] = None
    search: Optional[str] = None