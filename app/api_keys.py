from fastapi import HTTPException, Depends, status
from fastapi.security import APIKeyHeader
import os

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

API_KEYS = os.getenv("API_KEYS", "default-key").split(",")

async def get_api_key(api_key_header: str = Depends(api_key_header)) -> str:
    """Validate API key from header."""
    if api_key_header is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API Key required",
        )
    if api_key_header not in API_KEYS:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API Key",
        )
    return api_key_header
