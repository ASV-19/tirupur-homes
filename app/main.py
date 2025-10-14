# # app/main.py
# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from .config import settings
# from .database import engine, Base
# from .api.v1 import api_router

# # Create database tables
# Base.metadata.create_all(bind=engine)

# app = FastAPI(
#     title=settings.APP_NAME,
#     version="1.0.0",
#     docs_url="/docs",
#     redoc_url="/redoc"
# )

# # CORS middleware
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=settings.ALLOWED_ORIGINS,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Include API routes
# app.include_router(api_router, prefix=settings.API_V1_PREFIX)

# @app.get("/")
# def root():
#     return {
#         "message": "Tirupur Homes API",
#         "version": "1.0.0",
#         "docs": "/docs"
#     }

# @app.get("/health")
# def health_check():
#     return {"status": "healthy"}


#### MOCK ####

# app/main.py (Modified for testing without DB)
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .api.v1 import api_router

# Comment out database creation for pure API testing
# from .database import engine, Base
# Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix=settings.API_V1_PREFIX)

@app.get("/")
def root():
    return {
        "message": "Tirupur Homes API",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "running"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "database": "not connected (testing mode)"}