from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, status, Form
from fastapi.responses import JSONResponse
from typing import Optional
import os
import uuid

from app.pdf_processor import PDFProcessor
from app.auth import create_access_token, get_current_user
from app.api_keys import get_api_key
from app.rate_limit import rate_limiter
from app.models.base import PDFDocument, User
from app.schemas import (
    PDFUploadResponse,
    PDFConversionResponse,
    Token,
    UserCreate,
    UserResponse
)

router = APIRouter()

# Configure upload directory
UPLOAD_DIR = os.getenv("UPLOAD_DIR", "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.get("/health", response_model=dict, tags=["health"])
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": __import__("datetime").datetime.utcnow().isoformat()
    }

@router.post("/auth/register", response_model=UserResponse, tags=["auth"])
async def register_user(user: UserCreate):
    """Register a new user."""
    # In production, you'd want to hash the password
    return {
        "id": 1,
        "username": user.username,
        "email": user.email,
        "is_active": True,
        "created_at": __import__("datetime").datetime.utcnow()
    }

@router.post("/auth/token", response_model=Token, tags=["auth"])
async def login_for_access_token(
    username: str = Form(...),
    password: str = Form(...)
):
    """Get JWT access token."""
    # In production, validate credentials against database
    access_token = create_access_token(data={"sub": username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/upload", response_model=PDFUploadResponse, tags=["pdf-conversion"])
async def upload_pdf(
    file: UploadFile = File(...),
    api_key: str = Depends(get_api_key),
    rate_limited = Depends(rate_limiter)
):
    """Upload a PDF file for conversion."""
    if not file.filename.endswith(".pdf"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF files are allowed"
        )
    
    # Generate unique filename
    file_id = str(uuid.uuid4())
    filename = f"{file_id}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, filename)
    
    try:
        # Save uploaded file
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        return {
            "message": "PDF uploaded successfully",
            "document_id": hash(file_id),
            "status": "uploaded"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error saving file: {str(e)}"
        )

@router.post("/convert", response_model=PDFConversionResponse, tags=["pdf-conversion"])
async def convert_pdf(
    file: UploadFile = File(...),
    metadata: str = Form("{}"),
    api_key: str = Depends(get_api_key),
    rate_limited = Depends(rate_limiter)
):
    """Convert PDF to JSON format."""
    if not file.filename.endswith(".pdf"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF files are allowed"
        )
    
    file_id = str(uuid.uuid4())
    filename = f"{file_id}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, filename)
    
    try:
        # Save uploaded file
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        # Parse metadata
        import json
        try:
            metadata_dict = json.loads(metadata)
        except json.JSONDecodeError:
            metadata_dict = {}
        
        # Process PDF
        result = PDFProcessor.process_pdf(file_path)
        
        # Clean up
        os.remove(file_path)
        
        return {
            "document_id": hash(file_id),
            "filename": file.filename,
            "json_output": result,
            "status": "completed",
            "message": "PDF converted to JSON successfully"
        }
    
    except FileNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing PDF: {str(e)}"
        )

@router.post("/convert-url", response_model=PDFConversionResponse, tags=["pdf-conversion"])
async def convert_pdf_from_url(
    url: str = Form(...),
    metadata: str = Form("{}"),
    api_key: str = Depends(get_api_key),
    rate_limited = Depends(rate_limiter)
):
    """Convert PDF to JSON from URL."""
    import tempfile
    import requests
    
    try:
        # Download PDF from URL
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp_file:
            tmp_file.write(response.content)
            tmp_path = tmp_file.name
        
        # Parse metadata
        import json
        try:
            metadata_dict = json.loads(metadata)
        except json.JSONDecodeError:
            metadata_dict = {}
        
        # Process PDF
        result = PDFProcessor.process_pdf(tmp_path)
        
        # Clean up
        os.remove(tmp_path)
        
        # Extract filename from URL
        filename = url.split("/")[-1] or "document.pdf"
        
        return {
            "document_id": hash(url),
            "filename": filename,
            "json_output": result,
            "status": "completed",
            "message": "PDF from URL converted to JSON successfully"
        }
    
    except requests.RequestException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error downloading PDF: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing PDF: {str(e)}"
        )
