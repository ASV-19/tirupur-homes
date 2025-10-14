# app/crud/property.py
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from typing import List, Optional
from slugify import slugify
from ..models.property import Property, PropertyImage, PropertyType, PropertyStatus
from ..schemas.property import PropertyCreate, PropertyUpdate

def get_property(db: Session, property_id: int) -> Optional[Property]:
    return db.query(Property).filter(Property.id == property_id).first()

def get_property_by_slug(db: Session, slug: str) -> Optional[Property]:
    return db.query(Property).filter(Property.slug == slug).first()

def get_properties(
    db: Session,
    skip: int = 0,
    limit: int = 20,
    property_type: Optional[PropertyType] = None,
    status: PropertyStatus = PropertyStatus.AVAILABLE,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    min_bedrooms: Optional[int] = None,
    city: Optional[str] = None,
    search: Optional[str] = None,
    is_featured: Optional[bool] = None
) -> List[Property]:
    query = db.query(Property).filter(Property.status == status)
    
    if property_type:
        query = query.filter(Property.property_type == property_type)
    
    if min_price:
        query = query.filter(Property.price >= min_price)
    
    if max_price:
        query = query.filter(Property.price <= max_price)
    
    if min_bedrooms:
        query = query.filter(Property.bedrooms >= min_bedrooms)
    
    if city:
        query = query.filter(Property.city.ilike(f"%{city}%"))
    
    if is_featured is not None:
        query = query.filter(Property.is_featured == is_featured)
    
    if search:
        query = query.filter(
            or_(
                Property.title.ilike(f"%{search}%"),
                Property.description.ilike(f"%{search}%"),
                Property.address.ilike(f"%{search}%")
            )
        )
    
    return query.order_by(Property.created_at.desc()).offset(skip).limit(limit).all()

def create_property(db: Session, property: PropertyCreate, user_id: int) -> Property:
    # Generate unique slug
    base_slug = slugify(property.title)
    slug = base_slug
    counter = 1
    while db.query(Property).filter(Property.slug == slug).first():
        slug = f"{base_slug}-{counter}"
        counter += 1
    
    db_property = Property(
        **property.model_dump(),
        slug=slug,
        created_by_id=user_id
    )
    db.add(db_property)
    db.commit()
    db.refresh(db_property)
    return db_property

def update_property(
    db: Session,
    property_id: int,
    property_update: PropertyUpdate
) -> Optional[Property]:
    db_property = get_property(db, property_id)
    if not db_property:
        return None
    
    update_data = property_update.model_dump(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(db_property, key, value)
    
    db.commit()
    db.refresh(db_property)
    return db_property

def delete_property(db: Session, property_id: int) -> bool:
    db_property = get_property(db, property_id)
    if not db_property:
        return False
    
    db.delete(db_property)
    db.commit()
    return True

def add_property_image(
    db: Session,
    property_id: int,
    url: str,
    public_id: str,
    caption: Optional[str] = None,
    order: int = 0
) -> PropertyImage:
    db_image = PropertyImage(
        property_id=property_id,
        url=url,
        public_id=public_id,
        caption=caption,
        order=order
    )
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image