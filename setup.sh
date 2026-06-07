#!/bin/bash

# SAKHA AI - Quick Development Start Script

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== SAKHA AI Quick Start ===${NC}\n"

# Check Node.js
echo -e "${BLUE}Checking Node.js...${NC}"
if ! command -v node &> /dev/null; then
    echo "Node.js not found. Please install Node.js 18+"
    exit 1
fi
echo -e "${GREEN}✓ Node.js $(node -v)${NC}\n"

# Check Python
echo -e "${BLUE}Checking Python...${NC}"
if ! command -v python &> /dev/null; then
    echo "Python not found. Please install Python 3.10+"
    exit 1
fi
echo -e "${GREEN}✓ Python $(python --version)${NC}\n"

# Backend Setup
echo -e "${BLUE}Setting up Backend...${NC}"
cd backend
if [ ! -d "venv" ]; then
    python -m venv venv
fi
source venv/bin/activate
pip install -q -r requirements.txt
echo -e "${GREEN}✓ Backend dependencies installed${NC}\n"

# Frontend Setup
echo -e "${BLUE}Setting up Frontend...${NC}"
cd ../frontend
npm install -q
echo -e "${GREEN}✓ Frontend dependencies installed${NC}\n"

echo -e "${GREEN}✓ All set up!${NC}\n"
echo -e "${BLUE}To start developing:${NC}"
echo "Terminal 1: cd backend && python run.py"
echo "Terminal 2: cd frontend && npm run dev"
echo ""
echo "Backend API: http://localhost:8000"
echo "Frontend: http://localhost:5173"
echo "API Docs: http://localhost:8000/api/docs"
