#!/usr/bin/env python3
"""
SAKHA Bot Startup Script
"""
import sys
import os
from pathlib import Path

def check_requirements():
    """Check if all requirements are met"""
    print("🔍 Checking requirements...")
    
    # Check Python version
    if sys.version_info < (3, 12):
        print("❌ Python 3.12+ is required")
        return False
    print(f"✅ Python {sys.version.split()[0]}")
    
    # Check .env file
    if not Path(".env").exists():
        print("❌ .env file not found. Copy .env.example to .env and configure it")
        return False
    print("✅ .env file found")
    
    # Check dependencies
    try:
        import fastapi
        import pymongo
        import openai
        print("✅ Required packages installed")
    except ImportError as e:
        print(f"❌ Missing package: {e}")
        print("Run: pip install -r requirements.txt")
        return False
    
    return True


def initialize_directories():
    """Create necessary directories"""
    print("\n📁 Creating directories...")
    
    dirs = [
        "logs",
        "whatsapp_auth",
        "backups",
        "data"
    ]
    
    for dir_name in dirs:
        Path(dir_name).mkdir(exist_ok=True)
        print(f"✅ Created {dir_name}/")


def start_bot():
    """Start the SAKHA Bot"""
    print("\n🚀 Starting SAKHA Bot...\n")
    
    import uvicorn
    
    uvicorn.run(
        "sakha.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )


def main():
    """Main startup function"""
    print("""
╔══════════════════════════════════╗
║      SAKHA - Personal AI Bot     ║
║     Pranab Goswami Assistant     ║
╚══════════════════════════════════╝
""")
    
    # Check requirements
    if not check_requirements():
        print("\n❌ Requirements not met. Please fix the issues above.")
        sys.exit(1)
    
    # Initialize directories
    initialize_directories()
    
    # Start bot
    try:
        start_bot()
    except KeyboardInterrupt:
        print("\n\n👋 SAKHA Bot stopped. Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
