"""File model for SAKHA AI Premium"""

from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any, List


class FileModel(BaseModel):
    """File model for uploaded files"""
    id: Optional[str] = None
    user_id: str
    
    # File info
    filename: str
    original_filename: str
    file_type: str  # pdf, docx, txt, csv, json, image
    file_size: int  # in bytes
    mime_type: str
    
    # Storage
    file_path: str
    storage_provider: str = "local"  # local, s3, gcs, etc.
    
    # Analysis
    is_analyzed: bool = False
    analysis_summary: Optional[str] = None
    extracted_text: Optional[str] = None
    
    # Metadata
    pages: Optional[int] = None  # for PDFs
    language: Optional[str] = None
    encoding: Optional[str] = None
    
    # Organization
    tags: List[str] = []
    folder: Optional[str] = None
    
    # Usage tracking
    times_analyzed: int = 0
    last_analyzed: Optional[datetime] = None
    
    # Sharing
    is_shared: bool = False
    share_token: Optional[str] = None
    
    # Timestamps
    created_at: datetime
    updated_at: datetime
    expires_at: Optional[datetime] = None  # For temporary files
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "user_123",
                "filename": "document.pdf",
                "original_filename": "my-document.pdf",
                "file_type": "pdf",
                "file_size": 102400,
                "mime_type": "application/pdf"
            }
        }
