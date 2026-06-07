"""SAKHA AI - FastAPI Main Application"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging

from sakha.config import settings
from sakha.routes import chat, images, files, admin, health
from sakha.utils.logging_config import setup_logging

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Premium AI Assistant - Chat, Images, File Analysis",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Exception Handlers
@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle general exceptions"""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )


# Include Routes
app.include_router(health.router, prefix="/api", tags=["Health"])
app.include_router(chat.router, prefix="/api", tags=["Chat"])
app.include_router(images.router, prefix="/api", tags=["Images"])
app.include_router(files.router, prefix="/api", tags=["Files"])
app.include_router(admin.router, prefix="/api", tags=["Admin"])


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "version": settings.APP_VERSION,
        "docs": "/api/docs",
    }


@app.on_event("startup")
async def startup_event():
    """Run on startup"""
    from sakha.database.mongodb import mongodb
    
    logger.info(f"Starting {settings.APP_NAME}")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"Database: {settings.DATABASE_TYPE}")
    
    # Connect to MongoDB
    try:
        await mongodb.connect_db()
        logger.info("✓ Database connected successfully")
    except Exception as e:
        logger.error(f"✗ Failed to connect to database: {e}")
        raise


@app.on_event("shutdown")
async def shutdown_event():
    """Run on shutdown"""
    from sakha.database.mongodb import mongodb
    
    logger.info(f"Shutting down {settings.APP_NAME}")
    
    # Close MongoDB connection
    try:
        await mongodb.close_db()
        logger.info("✓ Database disconnected successfully")
    except Exception as e:
        logger.error(f"✗ Error closing database connection: {e}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "sakha.main:app",
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        reload=settings.DEBUG,
        log_level="info",
    )
