#!/bin/bash
# SAKHA AI - Production Deployment Script (Linux/Mac)
# Deploys both frontend to GitHub Pages and backend to Render/Railway

set -e  # Exit on error

echo ""
echo "========================================"
echo "  SAKHA AI - Production Deployment"
echo "========================================"
echo ""

# Check prerequisites
echo "Step 0: Checking prerequisites..."

if ! command -v git &> /dev/null; then
    echo "ERROR: Git is not installed"
    exit 1
fi

if ! command -v node &> /dev/null; then
    echo "ERROR: Node.js is not installed"
    exit 1
fi

if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    exit 1
fi

echo "✓ Prerequisites verified"

# Verify git repository
echo ""
echo "Step 1: Verifying repository setup..."
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "ERROR: Not a git repository"
    exit 1
fi
echo "✓ Git repository verified"

# Update and push code
echo ""
echo "Step 2: Updating code..."
git add .
git commit -m "Production deployment update" || true
git push origin main

# Deploy frontend
echo ""
echo "Step 3: Deploying frontend to GitHub Pages..."
cd frontend

echo "Installing dependencies..."
npm install

echo "Building for production..."
export VITE_REPO_NAME=${VITE_REPO_NAME:-sakha-ai}
export VITE_API_URL=${VITE_API_URL}
npm run build

echo "Deploying to GitHub Pages..."
npm run deploy

if [ $? -ne 0 ]; then
    echo "ERROR: GitHub Pages deployment failed"
    exit 1
fi

echo "✓ Frontend deployed successfully!"
cd ..

# Backend deployment instructions
echo ""
echo "Step 4: Backend deployment to Render/Railway..."
echo ""
echo "Options:"
echo "1) Render (Recommended - Free tier)"
echo "2) Railway"
echo "3) Skip"
echo ""
read -p "Select option (1-3): " backend_choice

case $backend_choice in
    1)
        echo ""
        echo "Render deployment instructions:"
        echo "1. Go to https://render.com"
        echo "2. Create New Web Service"
        echo "3. Connect your GitHub repository"
        echo "4. Set build command: pip install -r backend/requirements.txt"
        echo "5. Set start command: cd backend && python run.py"
        echo "6. Add environment variables from .env.example"
        echo "7. Deploy!"
        echo ""
        echo "Backend URL will be: https://YOUR_REPO_NAME.onrender.com"
        ;;
    2)
        echo ""
        echo "Railway deployment instructions:"
        echo "1. Install Railway CLI: npm install -g @railway/cli"
        echo "2. Run: railway login"
        echo "3. Run: railway link"
        echo "4. Run: railway up"
        echo "5. Set environment variables in dashboard"
        ;;
    3)
        echo "Skipping backend deployment"
        ;;
esac

echo ""
echo "========================================"
echo "  ✓ Deployment Complete!"
echo "========================================"
echo ""
echo "Frontend: https://YOUR_USERNAME.github.io/sakha-ai"
echo "API Docs: https://your-backend.onrender.com/api/docs"
echo ""
echo "Next steps:"
echo "1. Test your deployed frontend"
echo "2. Verify backend API is responding"
echo "3. Check database connectivity"
echo "4. Share with friends!"
echo ""
