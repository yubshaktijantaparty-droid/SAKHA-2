#!/bin/bash

# GitHub Pages + Render Deployment Setup Script
# This script helps you prepare SAKHA AI for GitHub Pages + Render deployment

set -e

echo "╔════════════════════════════════════════════════╗"
echo "║   SAKHA AI - GitHub Pages Setup              ║"
echo "║   Frontend: GitHub Pages                      ║"
echo "║   Backend: Render                             ║"
echo "╚════════════════════════════════════════════════╝"
echo ""

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo -e "${YELLOW}Git not initialized. Initializing...${NC}"
    git init
    echo -e "${GREEN}✓ Git initialized${NC}"
fi

# Step 1: GitHub Repository Setup
echo ""
echo -e "${YELLOW}Step 1: GitHub Repository Setup${NC}"
echo "Before continuing, you need to:"
echo "1. Create a new repository on GitHub: https://github.com/new"
echo "2. Name it 'sakha-ai' (or your preferred name)"
echo "3. Make it PUBLIC"
echo ""
read -p "Have you created the GitHub repository? (y/n) " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${RED}Please create a GitHub repository first.${NC}"
    exit 1
fi

# Get GitHub username and repo name
read -p "Enter your GitHub username: " GITHUB_USERNAME
read -p "Enter your repository name (default: sakha-ai): " REPO_NAME
REPO_NAME=${REPO_NAME:-sakha-ai}

# Step 2: Add remote and push
echo ""
echo -e "${YELLOW}Step 2: Pushing code to GitHub${NC}"
git remote remove origin 2>/dev/null || true
git remote add origin "https://github.com/$GITHUB_USERNAME/$REPO_NAME.git"
git add .
git commit -m "Initial commit: SAKHA AI ChatGPT website" --allow-empty
git branch -M main
git push -u origin main

echo -e "${GREEN}✓ Code pushed to GitHub${NC}"

# Step 3: Render Setup Instructions
echo ""
echo -e "${YELLOW}Step 3: Render Backend Setup${NC}"
echo "Visit: https://render.com"
echo ""
echo "Configuration:"
echo "  - Repository: https://github.com/$GITHUB_USERNAME/$REPO_NAME"
echo "  - Build Command: pip install -r requirements.txt"
echo "  - Start Command: cd backend && python run.py"
echo ""
echo "Required Environment Variables:"
echo "  - OPENAI_API_KEY or DEEPSEEK_API_KEY or GEMINI_API_KEY"
echo "  - MONGODB_URI (MongoDB Atlas)"
echo "  - CORS_ORIGINS=https://$GITHUB_USERNAME.github.io"
echo ""
read -p "Enter your Render Backend URL (https://sakha-backend-xxxx.onrender.com): " RENDER_URL

# Step 4: GitHub Actions Secrets
echo ""
echo -e "${YELLOW}Step 4: GitHub Secrets Configuration${NC}"
echo "Visit: https://github.com/$GITHUB_USERNAME/$REPO_NAME/settings/secrets/actions"
echo ""
echo "Create these secrets:"
echo "  1. VITE_API_URL = $RENDER_URL"
echo "  2. VITE_REPO_NAME = $REPO_NAME"
echo "  3. RENDER_DEPLOY_KEY = (from Render settings)"
echo "  4. CUSTOM_DOMAIN = (optional, for custom domain)"
echo ""
read -p "Have you configured GitHub Secrets? (y/n) " -n 1 -r
echo ""

# Step 5: Update environment files
echo ""
echo -e "${YELLOW}Step 5: Updating Configuration${NC}"

# Update .env.production
sed -i "s|VITE_API_URL=.*|VITE_API_URL=$RENDER_URL|g" .env.production
sed -i "s|VITE_REPO_NAME=.*|VITE_REPO_NAME=$REPO_NAME|g" .env.production

echo -e "${GREEN}✓ Configuration files updated${NC}"

# Step 6: Enable GitHub Pages
echo ""
echo -e "${YELLOW}Step 6: Enable GitHub Pages${NC}"
echo "Visit: https://github.com/$GITHUB_USERNAME/$REPO_NAME/settings/pages"
echo ""
echo "Settings:"
echo "  - Source: GitHub Actions (should be default)"
echo "  - Custom domain: (optional)"
echo ""
read -p "Have you enabled GitHub Pages? (y/n) " -n 1 -r
echo ""

# Final summary
echo ""
echo "╔════════════════════════════════════════════════╗"
echo "║         Setup Complete! 🎉                    ║"
echo "╚════════════════════════════════════════════════╝"
echo ""
echo "Your deployment URLs:"
echo -e "${GREEN}Frontend: https://$GITHUB_USERNAME.github.io/$REPO_NAME${NC}"
echo -e "${GREEN}Backend: $RENDER_URL${NC}"
echo -e "${GREEN}API Docs: $RENDER_URL/api/docs${NC}"
echo ""
echo "Next steps:"
echo "1. Wait for GitHub Actions workflow to complete (Actions tab)"
echo "2. Verify Render backend is running"
echo "3. Test your application"
echo ""
echo "For detailed information, see: GITHUB_PAGES_DEPLOYMENT.md"
echo ""
