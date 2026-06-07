"""
Quick Start Script for SAKHA Bot
Run this to get started quickly!
"""
import os
import subprocess
import sys
from pathlib import Path


def print_header():
    print("""
╔════════════════════════════════════════╗
║   SAKHA - Personal AI Assistant Bot   ║
║   Quick Start Configuration            ║
╚════════════════════════════════════════╝
""")


def check_python():
    """Check Python version"""
    if sys.version_info < (3, 12):
        print("❌ Python 3.12+ required")
        print(f"   Current: Python {sys.version.split()[0]}")
        return False
    print(f"✅ Python {sys.version.split()[0]}")
    return True


def create_env_file():
    """Create .env file if not exists"""
    if Path(".env").exists():
        print("✅ .env file exists")
        return True
    
    if not Path(".env.example").exists():
        print("❌ .env.example not found")
        return False
    
    print("📝 Creating .env file from template...")
    with open(".env.example") as f:
        content = f.read()
    with open(".env", "w") as f:
        f.write(content)
    print("✅ .env file created (⚠️ Please update it with your API keys)")
    return True


def install_requirements():
    """Install Python dependencies"""
    print("\n📦 Installing dependencies...")
    
    if not Path("requirements.txt").exists():
        print("❌ requirements.txt not found")
        return False
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False


def create_directories():
    """Create necessary directories"""
    print("\n📁 Creating directories...")
    dirs = ["logs", "whatsapp_auth", "backups"]
    for dir_name in dirs:
        Path(dir_name).mkdir(exist_ok=True)
    print(f"✅ Created {len(dirs)} directories")


def show_next_steps():
    """Show next steps"""
    print("""
✅ Setup Complete! Next steps:

1. 📝 Edit .env file with your settings:
   - Add MongoDB URI
   - Add OpenAI API key
   - Set bot owner ID

2. ▶️ Run the bot:
   python run.py
   
   Or with uvicorn:
   uvicorn sakha.main:app --reload

3. 🔗 Access the API:
   http://localhost:8000
   
   API Docs:
   http://localhost:8000/docs

4. 📚 Read documentation:
   - README.md - Overview
   - SETUP_GUIDE.md - Detailed setup
   - API_DOCUMENTATION.md - API reference
   - ARCHITECTURE.md - System design

📧 For support: contact@example.com
""")


def main():
    """Main quickstart"""
    print_header()
    
    # Check Python
    if not check_python():
        sys.exit(1)
    
    # Create env file
    if not create_env_file():
        sys.exit(1)
    
    # Install dependencies
    if not install_requirements():
        sys.exit(1)
    
    # Create directories
    create_directories()
    
    # Show next steps
    show_next_steps()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Setup cancelled")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
