"""File Analysis Endpoints"""

from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import Optional
import os

from sakha.services.file_service import FileService
from sakha.config import settings

router = APIRouter()
file_service = FileService()


class FileAnalysisRequest(BaseModel):
    """File analysis request"""

    action: str  # summarize, analyze, extract, answer
    question: Optional[str] = None


@router.post("/files/upload")
async def upload_file(file: UploadFile = File(...)):
    """Upload a file for analysis"""
    try:
        # Validate file type
        allowed_types = [
            "application/pdf",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "text/plain",
            "image/jpeg",
            "image/png",
            "text/csv",
        ]

        if file.content_type not in allowed_types:
            raise HTTPException(status_code=400, detail="File type not supported")

        # Save file
        file_path = await file_service.save_file(file)

        return {
            "file_id": file.filename,
            "file_path": file_path,
            "file_type": file.content_type,
            "message": "File uploaded successfully",
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/files/{file_id}/analyze")
async def analyze_file(file_id: str, request: FileAnalysisRequest):
    """Analyze an uploaded file"""
    try:
        result = await file_service.analyze_file(
            file_id=file_id,
            action=request.action,
            question=request.question,
        )

        return {"file_id": file_id, "analysis": result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/files/supported")
async def get_supported_file_types():
    """Get list of supported file types"""
    return {
        "supported_types": [
            {"type": "PDF", "extension": ".pdf"},
            {"type": "Word Document", "extension": ".docx"},
            {"type": "Text", "extension": ".txt"},
            {"type": "Image", "extension": ".jpg, .png"},
            {"type": "CSV", "extension": ".csv"},
        ]
    }
