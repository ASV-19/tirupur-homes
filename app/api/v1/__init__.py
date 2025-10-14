# app/api/v1/__init__.py
from fastapi import APIRouter
from .properties import router as properties_router
from .auth import router as auth_router
from .upload import router as upload_router
from .inquiries import router as inquiries_router

api_router = APIRouter()

api_router.include_router(auth_router)
api_router.include_router(properties_router)
api_router.include_router(upload_router)
api_router.include_router(inquiries_router)