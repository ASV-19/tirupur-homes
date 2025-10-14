# # app/api/v1/auth.py
# from fastapi import APIRouter, Depends, HTTPException, status
# from fastapi.security import OAuth2PasswordRequestForm
# from sqlalchemy.orm import Session
# from datetime import timedelta
# from ...database import get_db
# from ...schemas.user import UserCreate, UserResponse, Token
# from ...crud.user import get_user_by_email, create_user
# from ...core.security import verify_password, create_access_token
# from ...config import settings

# router = APIRouter(prefix="/auth", tags=["Authentication"])

# @router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
# def register(user: UserCreate, db: Session = Depends(get_db)):
#     """Register new admin user"""
#     db_user = get_user_by_email(db, email=user.email)
#     if db_user:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Email already registered"
#         )
    
#     return create_user(db=db, user=user)

# @router.post("/login", response_model=Token)
# def login(
#     form_data: OAuth2PasswordRequestForm = Depends(),
#     db: Session = Depends(get_db)
# ):
#     """Login and get access token"""
#     user = get_user_by_email(db, email=form_data.username)
    
#     if not user or not verify_password(form_data.password, user.hashed_password):
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect email or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
    
#     access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(
#         data={"sub": user.email},
#         expires_delta=access_token_expires
#     )
    
#     return {"access_token": access_token, "token_type": "bearer"}


#### MOCK ####

# app/api/v1/auth.py (Mock version)
from fastapi import APIRouter, HTTPException, status
from ...schemas.user import Token

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login", response_model=Token)
def login_mock(email: str, password: str):
    """Mock login - returns dummy token"""
    
    # Simple mock validation
    if email == "admin@tirupurhomes.com" and password == "admin123":
        return {
            "access_token": "mock-jwt-token-for-testing-purposes",
            "token_type": "bearer"
        }
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect email or password"
    )

@router.post("/register")
def register_mock(email: str, name: str, password: str):
    """Mock registration"""
    return {
        "id": 1,
        "email": email,
        "name": name,
        "role": "ADMIN",
        "message": "User registered successfully (MOCK)"
    }