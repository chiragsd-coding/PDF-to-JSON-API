from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import api

app = FastAPI(
    title="PDF to JSON API",
    description="API for converting PDF documents to structured JSON format",
    version="1.0.0"
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api.router, prefix="/api/v1", tags=["pdf-conversion"])
