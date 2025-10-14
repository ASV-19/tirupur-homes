# app/schemas/inquiry.py
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional
from datetime import datetime

class InquiryBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    phone: str = Field(..., min_length=10, max_length=20)
    message: str = Field(..., min_length=10)

class InquiryCreate(InquiryBase):
    property_id: Optional[int] = None

class InquiryResponse(InquiryBase):
    id: int
    property_id: Optional[int]
    is_read: bool
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)