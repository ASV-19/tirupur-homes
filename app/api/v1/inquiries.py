# # app/api/v1/inquiries.py
# from fastapi import APIRouter, Depends, HTTPException, status
# from sqlalchemy.orm import Session
# from typing import List
# from ...database import get_db
# from ...schemas.inquiry import InquiryCreate, InquiryResponse
# from ...models.inquiry import ContactInquiry
# from ...dependencies import get_current_active_user

# router = APIRouter(prefix="/inquiries", tags=["Inquiries"])

# @router.post("/", response_model=InquiryResponse, status_code=status.HTTP_201_CREATED)
# def create_inquiry(inquiry: InquiryCreate, db: Session = Depends(get_db)):
#     """Create contact inquiry (public endpoint)"""
#     db_inquiry = ContactInquiry(**inquiry.model_dump())
#     db.add(db_inquiry)
#     db.commit()
#     db.refresh(db_inquiry)
#     return db_inquiry

# @router.get("/", response_model=List[InquiryResponse])
# def list_inquiries(
#     skip: int = 0,
#     limit: int = 50,
#     current_user = Depends(get_current_active_user),
#     db: Session = Depends(get_db)
# ):
#     """Get all inquiries (Admin only)"""
#     inquiries = db.query(ContactInquiry).order_by(
#         ContactInquiry.created_at.desc()
#     ).offset(skip).limit(limit).all()
#     return inquiries

# @router.patch("/{inquiry_id}/read")
# def mark_inquiry_as_read(
#     inquiry_id: int,
#     current_user = Depends(get_current_active_user),
#     db: Session = Depends(get_db)
# ):
#     """Mark inquiry as read (Admin only)"""
#     inquiry = db.query(ContactInquiry).filter(ContactInquiry.id == inquiry_id).first()
#     if not inquiry:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Inquiry not found"
#         )
    
#     inquiry.is_read = True
#     db.commit()
#     return {"message": "Inquiry marked as read"}


#### MOCK ####

# app/api/v1/inquiries.py (Mock version)
from fastapi import APIRouter, status
from typing import List
from ...schemas.inquiry import InquiryCreate, InquiryResponse

router = APIRouter(prefix="/inquiries", tags=["Inquiries"])

MOCK_INQUIRIES = []

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_inquiry(inquiry: InquiryCreate):
    """Create inquiry (MOCK - stores in memory)"""
    inquiry_dict = inquiry.model_dump()
    inquiry_dict["id"] = len(MOCK_INQUIRIES) + 1
    inquiry_dict["is_read"] = False
    inquiry_dict["created_at"] = "2024-01-15T10:30:00"
    MOCK_INQUIRIES.append(inquiry_dict)
    return inquiry_dict

@router.get("/", response_model=List[InquiryResponse])
def list_inquiries():
    """Get all inquiries (MOCK)"""
    return MOCK_INQUIRIES

@router.patch("/{inquiry_id}/read")
def mark_inquiry_as_read(inquiry_id: int):
    """Mark inquiry as read (MOCK)"""
    return {"message": "Inquiry marked as read", "id": inquiry_id}