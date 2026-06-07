#!/usr/bin/env python3
"""Run the SAKHA AI backend server"""

import sys
import os

# Add backend directory to path
sys.path.insert(0, os.path.dirname(__file__))

import uvicorn
from sakha.main import app
from sakha.config import settings

if __name__ == "__main__":
    print(f"Starting {settings.APP_NAME} API Server...")
    print(f"Environment: {settings.ENVIRONMENT}")
    print(f"Server: {settings.SERVER_HOST}:{settings.SERVER_PORT}")
    print(f"Docs: http://{settings.SERVER_HOST}:{settings.SERVER_PORT}/api/docs")

    uvicorn.run(
        "sakha.main:app",
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        reload=settings.DEBUG,
        log_level="info",
    )
