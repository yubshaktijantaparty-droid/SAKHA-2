@echo off
REM GitHub Pages + Render Deployment Setup Script (Windows)
REM This script helps you prepare SAKHA AI for GitHub Pages + Render deployment

setlocal enabledelayedexpansion

echo.
echo ====================================================
echo    SAKHA AI - GitHub Pages Setup (Windows)
echo    Frontend: GitHub Pages
echo    Backend: Render
echo ====================================================
echo.

REM Check if git is initialized
if not exist ".git" (
    echo Initializing Git repository...
    git init
    echo [OK] Git initialized
)

REM Step 1: GitHub Repository Setup
echo.
echo Step 1: GitHub Repository Setup
echo Before continuing, you need to:
echo 1. Create a new repository on GitHub: https://github.com/new
echo 2. Name it 'sakha-ai' ^(or your preferred name^)
echo 3. Make it PUBLIC
echo.
set /p confirm="Have you created the GitHub repository? (y/n): "
if /i not "%confirm%"=="y" (
    echo Please create a GitHub repository first.
    exit /b 1
)

REM Get GitHub username and repo name
echo.
set /p GITHUB_USERNAME="Enter your GitHub username: "
set /p REPO_NAME="Enter your repository name (default: sakha-ai): "
if "%REPO_NAME%"=="" set REPO_NAME=sakha-ai

REM Step 2: Add remote and push
echo.
echo Step 2: Pushing code to GitHub
git remote remove origin 2>nul
git remote add origin "https://github.com/%GITHUB_USERNAME%/%REPO_NAME%.git"
git add .
git commit -m "Initial commit: SAKHA AI ChatGPT website" --allow-empty
git branch -M main
git push -u origin main

echo [OK] Code pushed to GitHub

REM Step 3: Render Setup Instructions
echo.
echo Step 3: Render Backend Setup
echo Visit: https://render.com
echo.
echo Configuration:
echo   - Repository: https://github.com/%GITHUB_USERNAME%/%REPO_NAME%
echo   - Build Command: pip install -r requirements.txt
echo   - Start Command: cd backend ^&& python run.py
echo.
echo Required Environment Variables:
echo   - OPENAI_API_KEY or DEEPSEEK_API_KEY or GEMINI_API_KEY
echo   - MONGODB_URI ^(MongoDB Atlas^)
echo   - CORS_ORIGINS=https://%GITHUB_USERNAME%.github.io
echo.
set /p RENDER_URL="Enter your Render Backend URL (https://sakha-backend-xxxx.onrender.com): "

REM Step 4: GitHub Actions Secrets
echo.
echo Step 4: GitHub Secrets Configuration
echo Visit: https://github.com/%GITHUB_USERNAME%/%REPO_NAME%/settings/secrets/actions
echo.
echo Create these secrets:
echo   1. VITE_API_URL = %RENDER_URL%
echo   2. VITE_REPO_NAME = %REPO_NAME%
echo   3. RENDER_DEPLOY_KEY = ^(from Render settings^)
echo   4. CUSTOM_DOMAIN = ^(optional, for custom domain^)
echo.
set /p confirm="Have you configured GitHub Secrets? (y/n): "

REM Step 5: Update environment files
echo.
echo Step 5: Updating Configuration
REM Create .env.production with proper values
(
    echo # SAKHA AI - Production Configuration
    echo # GitHub Pages + Render Deployment
    echo.
    echo VITE_API_URL=%RENDER_URL%
    echo VITE_REPO_NAME=%REPO_NAME%
    echo.
    echo SERVER_HOST=0.0.0.0
    echo SERVER_PORT=8000
    echo ENVIRONMENT=production
    echo DEBUG_MODE=False
    echo.
    echo OPENAI_API_KEY=sk-your-key-here
    echo DEEPSEEK_API_KEY=sk-your-key-here
    echo GEMINI_API_KEY=your-key-here
    echo DEFAULT_AI_PROVIDER=openai
    echo.
    echo MONGODB_URI=mongodb+srv://user:pass@cluster.mongodb.net/sakha_db
    echo MONGODB_DB_NAME=sakha_db
    echo.
    echo CORS_ORIGINS=https://%GITHUB_USERNAME%.github.io,%RENDER_URL%
) > .env.production

echo [OK] Configuration files updated

REM Step 6: Enable GitHub Pages
echo.
echo Step 6: Enable GitHub Pages
echo Visit: https://github.com/%GITHUB_USERNAME%/%REPO_NAME%/settings/pages
echo.
echo Settings:
echo   - Source: GitHub Actions
echo   - Custom domain: ^(optional^)
echo.
set /p confirm="Have you enabled GitHub Pages? (y/n): "

REM Final summary
echo.
echo ====================================================
echo          Setup Complete! 
echo ====================================================
echo.
echo Your deployment URLs:
echo Frontend: https://%GITHUB_USERNAME%.github.io/%REPO_NAME%
echo Backend: %RENDER_URL%
echo API Docs: %RENDER_URL%/api/docs
echo.
echo Next steps:
echo 1. Wait for GitHub Actions workflow to complete ^(Actions tab^)
echo 2. Verify Render backend is running
echo 3. Test your application
echo.
echo For detailed information, see: GITHUB_PAGES_DEPLOYMENT.md
echo.
pause
