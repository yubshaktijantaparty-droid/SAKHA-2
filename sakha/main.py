"""
SAKHA Bot - Main Application
"""
from fastapi import FastAPI, WebSocket, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, PlainTextResponse
import os
from contextlib import asynccontextmanager
import asyncio
from datetime import datetime

from sakha.config import settings
from sakha.database import db_manager, get_mongodb_ops, MongoDBOperations
from sakha.ai import ai_service
from sakha.handlers import CommandHandler, AdminCommandHandler
from sakha.whatsapp import whatsapp_manager, WhatsAppMessage
from sakha.admin import admin_command_handler
from sakha.utils import logger, parse_command, sanitize_input, ResponseFormatter


# Lifespan events
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan"""
    # Startup
    logger.info("🚀 SAKHA Bot Starting...")
    
    try:
        # Connect to database
        await db_manager.connect()
        
        # Start WhatsApp manager
        await whatsapp_manager.start()
        
        logger.info("✅ SAKHA Bot Started Successfully!")
    except Exception as e:
        logger.error(f"❌ Startup Error: {e}")
        raise
    
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down SAKHA Bot...")
    try:
        await db_manager.disconnect()
        logger.info("✅ Database disconnected")
    except Exception as e:
        logger.error(f"❌ Shutdown Error: {e}")


# Create FastAPI app
app = FastAPI(
    title="SAKHA - Personal AI Assistant Bot",
    description="WhatsApp-based personal AI assistant",
    version="1.0.0",
    lifespan=lifespan
)


# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins.split(",") if settings.cors_origins != "*" else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Global handlers
command_handler: CommandHandler = None
admin_handler: AdminCommandHandler = None


@app.on_event("startup")
async def initialize_handlers():
    """Initialize handlers"""
    global command_handler, admin_handler
    
    db_ops = await get_mongodb_ops()
    command_handler = CommandHandler(db_ops, ai_service)
    admin_handler = admin_command_handler


# Webhook verification and receiver for WhatsApp callbacks
VERIFY_TOKEN = os.getenv("WHATSAPP_VERIFY_TOKEN") or getattr(settings, "whatsapp_verify_token", None)


@app.get("/webhook")
async def verify_webhook(
    hub_mode: str | None = None,
    hub_verify_token: str | None = None,
    hub_challenge: str | None = None,
    hub_mode_q: str | None = None,
    hub_verify_token_q: str | None = None,
    hub_challenge_q: str | None = None,
):
    # Some providers send params twice; accept either name
    token = hub_verify_token or hub_verify_token_q
    challenge = hub_challenge or hub_challenge_q

    if token and VERIFY_TOKEN and token == VERIFY_TOKEN:
        return PlainTextResponse(challenge or "")
    return PlainTextResponse("Forbidden", status_code=403)


@app.post("/webhook")
async def webhook(request: Request):
    try:
        data = await request.json()
    except Exception:
        data = {}
    logger.info(f"Webhook received: {data}")
    # Simple echo response for webhook reception
    return {"status": "ok"}


# Routes

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": settings.bot_name,
        "owner": settings.bot_owner,
        "status": "🟢 Online",
        "version": "1.0.0"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "bot_name": settings.bot_name
    }


@app.get("/api/users/{user_id}")
async def get_user(user_id: str):
    """Get user profile"""
    try:
        db_ops = await get_mongodb_ops()
        user = await db_ops.get_user(user_id)
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        return {
            "status": "success",
            "data": user
        }
    except Exception as e:
        logger.error(f"Error getting user: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving user")


@app.post("/api/message")
async def handle_message(request: Request):
    """Handle incoming message"""
    try:
        data = await request.json()
        
        user_id = data.get("user_id")
        message_text = data.get("message", "").strip()
        
        if not user_id or not message_text:
            raise HTTPException(status_code=400, detail="Missing required fields")
        
        # Sanitize input
        message_text = sanitize_input(message_text)
        
        # Parse command
        command, args = parse_command(message_text, settings.bot_prefix)
        
        # Handle command or regular message
        if command:
            response = await handle_command(user_id, command, args)
        else:
            # Regular AI chat
            response = await command_handler.handle_ai(user_id, message_text)
        
        # Send response via WhatsApp
        await whatsapp_manager.send_text(user_id, response)
        
        return {
            "status": "success",
            "response": response
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error handling message: {e}")
        error_response = ResponseFormatter.error("An error occurred while processing your message")
        return {
            "status": "error",
            "response": error_response
        }


async def handle_command(user_id: str, command: str, args: str) -> str:
    """Handle user command"""
    try:
        # Check if admin command
        if command in ["admin", "broadcast", "ban", "unban", "stats", "restart", "logs", "settings"]:
            return await admin_handler.handle_admin_command(user_id, command, args)
        
        # Regular commands
        handlers = {
            "help": lambda: command_handler.handle_help(user_id),
            "menu": lambda: command_handler.handle_menu(user_id),
            "ai": lambda: command_handler.handle_ai(user_id, args),
            "ask": lambda: command_handler.handle_ai(user_id, args),
            "translate": lambda: command_handler.handle_translate(args.split()[0] if args else "", "es"),
            "study": lambda: command_handler.handle_study(user_id, args or None),
            "notes": lambda: command_handler.handle_notes(user_id, args or "list"),
            "todo": lambda: command_handler.handle_todo(user_id, args or "list"),
            "reminder": lambda: command_handler.handle_reminder(user_id, args),
            "weather": lambda: command_handler.handle_weather(),
            "news": lambda: command_handler.handle_news(),
            "quote": lambda: command_handler.handle_quote(),
            "joke": lambda: command_handler.handle_joke(),
            "time": lambda: command_handler.handle_time(),
            "date": lambda: command_handler.handle_date(),
        }
        
        handler = handlers.get(command.lower())
        if handler:
            return await handler()
        else:
            return ResponseFormatter.error(f"Unknown command: {command}. Use .help for available commands")
    
    except Exception as e:
        logger.error(f"Error handling command {command}: {e}")
        return ResponseFormatter.error(f"Error executing command: {str(e)[:50]}")


@app.post("/api/broadcast")
async def send_broadcast(request: Request):
    """Admin: Send broadcast message"""
    try:
        data = await request.json()
        
        admin_id = data.get("admin_id")
        message = data.get("message")
        
        if not admin_id or not message:
            raise HTTPException(status_code=400, detail="Missing required fields")
        
        # Verify admin
        from sakha.admin import admin_system
        if not admin_system.is_admin(admin_id):
            raise HTTPException(status_code=403, detail="Not authorized")
        
        # Send broadcast (in production, this would be queued)
        success = await admin_handler.admin_system.send_broadcast(message, admin_id)
        
        return {
            "status": "success" if success else "error",
            "message": "Broadcast sent" if success else "Failed to send broadcast"
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error sending broadcast: {e}")
        raise HTTPException(status_code=500, detail="Error sending broadcast")


@app.post("/api/stats")
async def get_stats(request: Request):
    """Admin: Get statistics"""
    try:
        data = await request.json()
        admin_id = data.get("admin_id")
        
        from sakha.admin import admin_system
        if not admin_system.is_admin(admin_id):
            raise HTTPException(status_code=403, detail="Not authorized")
        
        analytics = await admin_system.view_analytics(admin_id)
        
        return {
            "status": "success",
            "data": analytics
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving statistics")


@app.post("/webhook/whatsapp")
async def whatsapp_webhook(request: Request):
    """WhatsApp webhook"""
    try:
        data = await request.json()
        
        # Parse incoming message
        user_id = data.get("from", "")
        message_text = data.get("body", "")
        message_type = data.get("type", "text")
        
        if not user_id or not message_text:
            return {"status": "received"}
        
        # Create WhatsApp message
        wa_message = WhatsAppMessage(
            sender_id=user_id,
            text=message_text,
            message_type=message_type
        )
        
        # Handle message
        await whatsapp_manager.handle_message(wa_message)
        
        return {"status": "received"}
    
    except Exception as e:
        logger.error(f"Webhook error: {e}")
        return {"status": "error", "message": str(e)}


# Error handlers

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"status": "error", "detail": exc.detail}
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"status": "error", "detail": "Internal server error"}
    )


# Run the app
if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        app,
        host=settings.server_host,
        port=settings.server_port,
        reload=settings.reload_on_change and settings.debug_mode
    )
