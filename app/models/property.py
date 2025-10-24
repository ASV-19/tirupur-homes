# app/models/property.py
from sqlalchemy import Column, Integer, String, Text, Boolean, Numeric, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from ..database import Base

class PropertyType(str, enum.Enum):
    BUY = "BUY"
    SELL = "SELL"
    RENT = "RENT"

class PropertyStatus(str, enum.Enum):
    AVAILABLE = "AVAILABLE"
    SOLD = "SOLD"
    RENTED = "RENTED"
    PENDING = "PENDING"

class Property(Base):
    __tablename__ = "properties"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False, index=True)
    slug = Column(String(200), unique=True, index=True)
    description = Column(Text)
    price = Column(Numeric(10, 2), nullable=False)
    property_type = Column(Enum(PropertyType), nullable=False, index=True)
    status = Column(Enum(PropertyStatus), default=PropertyStatus.AVAILABLE, index=True)
    
    # Location
    address = Column(String(255))
    city = Column(String(100), default="Tirupur", index=True)
    state = Column(String(100), default="Tamil Nadu")
    zip_code = Column(String(10))
    
    # Details
    bedrooms = Column(Integer, default=1)
    bathrooms = Column(Integer, default=1)
    area = Column(Integer)  # in square feet
    
    # Features
    parking = Column(Boolean, default=False)
    furnished = Column(Boolean, default=False)
    
    # Status flags
    is_featured = Column(Boolean, default=False, index=True)
    is_special_offer = Column(Boolean, default=False)
    offer_text = Column(String(200))
    
    # Relationships
    created_by_id = Column(Integer, ForeignKey("users.id"))
    created_by = relationship("User", back_populates="properties")
    images = relationship("PropertyImage", back_populates="property", cascade="all, delete-orphan")
    inquiries = relationship("ContactInquiry", back_populates="property", cascade="all, delete-orphan")
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class PropertyImage(Base):
    __tablename__ = "property_images"
    
    id = Column(Integer, primary_key=True, index=True)
    property_id = Column(Integer, ForeignKey("properties.id", ondelete="CASCADE"))
    url = Column(String(500), nullable=False)
    public_id = Column(String(255))
    caption = Column(String(200))
    order = Column(Integer, default=0)
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())
    
    property = relationship("Property", back_populates="images")