#!/bin/bash
# SAKHA AI - Local Development Setup Script

set -e

echo ""
echo "========================================"
echo "  SAKHA AI - Development Setup"
echo "========================================"
echo ""

# Check prerequisites
echo "Checking prerequisites..."

if ! command -v git &> /dev/null; then
    echo "ERROR: Git not found. Please install Git."
    exit 1
fi

if ! command -v node &> /dev/null; then
    echo "ERROR: Node.js not found. Please install Node.js 18+."
    exit 1
fi

if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 not found. Please install Python 3.10+."
    exit 1
fi

echo "✓ All prerequisites found"

# Setup backend
echo ""
echo "Step 1: Setting up backend..."
cd backend

echo "Creating Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "✓ Backend setup complete"
cd ..

# Setup frontend
echo ""
echo "Step 2: Setting up frontend..."
cd frontend

echo "Installing Node dependencies..."
npm install

echo "✓ Frontend setup complete"
cd ..

# Setup environment
echo ""
echo "Step 3: Setting up environment variables..."

if [ ! -f .env ]; then
    echo "Creating .env from .env.example..."
    cp .env.example .env
    echo ""
    echo "⚠️  Please edit .env and add your API keys:"
    echo "   - OPENAI_API_KEY"
    echo "   - GEMINI_API_KEY or DEEPSEEK_API_KEY"
    echo "   - MONGODB_URI"
    echo "   - SUPABASE_URL and keys"
    echo ""
else
    echo "✓ .env file exists"
fi

echo ""
echo "========================================"
echo "  ✓ Setup Complete!"
echo "========================================"
echo ""
echo "To start development:"
echo ""
echo "  Terminal 1 - Backend:"
echo "    cd backend && source venv/bin/activate && python run.py"
echo ""
echo "  Terminal 2 - Frontend:"
echo "    cd frontend && npm run dev"
echo ""
echo "  Then open: http://localhost:5173"
echo ""
