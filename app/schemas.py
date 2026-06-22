from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    username: Optional[str] = None

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., email=True, max_length=100)
    password: str = Field(..., min_length=8)

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class APIKeyCreate(BaseModel):
    key: str

class APIKeyResponse(BaseModel):
    id: int
    key: str
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class PDFDocumentResponse(BaseModel):
    id: int
    filename: str
    status: str
    json_output: Optional[Dict[Any, Any]] = None
    created_at: datetime
    completed_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class PDFUploadResponse(BaseModel):
    message: str
    document_id: int
    status: str

class PDFConversionRequest(BaseModel):
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)

class PDFConversionResponse(BaseModel):
    document_id: int
    filename: str
    json_output: Dict[Any, Any]
    status: str
    message: str

class ErrorResponse(BaseModel):
    detail: str

class HealthCheckResponse(BaseModel):
    status: str
    timestamp: datetime