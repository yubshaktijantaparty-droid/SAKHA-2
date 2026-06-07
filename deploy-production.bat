@echo off
REM SAKHA AI - Production Deployment Script (Windows)
REM Deploys both frontend to GitHub Pages and backend to Render

echo.
echo ========================================
echo   SAKHA AI - Production Deployment
echo ========================================
echo.

REM Check if git is installed
git --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Git is not installed or not in PATH
    exit /b 1
)

REM Check Node.js
node --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js is not installed
    exit /b 1
)

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed
    exit /b 1
)

echo ✓ Prerequisites verified

echo.
echo Step 1: Verifying repository setup...
git status >nul 2>&1
if errorlevel 1 (
    echo ERROR: Not a git repository
    exit /b 1
)

echo ✓ Git repository verified

echo.
echo Step 2: Updating code...
git add .
git commit -m "Production deployment update" 2>nul
git push origin main

echo.
echo Step 3: Deploying frontend to GitHub Pages...
cd frontend

echo Installing dependencies...
call npm install

echo Building for production...
set VITE_REPO_NAME=sakha-ai
set VITE_API_URL=%VITE_API_URL%
call npm run build

if errorlevel 1 (
    echo ERROR: Frontend build failed
    exit /b 1
)

echo Deploying to GitHub Pages...
call npm run deploy

if errorlevel 1 (
    echo ERROR: GitHub Pages deployment failed
    exit /b 1
)

echo ✓ Frontend deployed successfully!
cd ..

echo.
echo Step 4: Backend deployment to Render/Railway...
echo.
echo Options:
echo 1) Render (Recommended - Free tier with 0.5 CPU/512MB RAM)
echo 2) Railway (0.5 credits free/month)
echo 3) Skip backend deployment
echo.
set /p backend="Select option (1-3): "

if "%backend%"=="1" (
    echo.
    echo Render deployment instructions:
    echo 1. Go to https://render.com
    echo 2. Create New Web Service
    echo 3. Connect your GitHub repository
    echo 4. Set build command: pip install -r backend/requirements.txt
    echo 5. Set start command: cd backend ^&^& python run.py
    echo 6. Add environment variables from .env.example
    echo 7. Deploy!
    echo.
    echo Backend URL will be: https://YOUR_REPO_NAME.onrender.com
) else if "%backend%"=="2" (
    echo.
    echo Railway deployment instructions:
    echo 1. Install Railway CLI: npm install -g @railway/cli
    echo 2. Run: railway login
    echo 3. Run: railway link
    echo 4. Run: railway up
    echo 5. Set environment variables in dashboard
) else (
    echo Skipping backend deployment.
)

echo.
echo ========================================
echo   ✓ Deployment Complete!
echo ========================================
echo.
echo Frontend: https://YOUR_USERNAME.github.io/sakha-ai
echo API Docs: https://your-backend.onrender.com/api/docs
echo.
echo Next steps:
echo 1. Test your deployed frontend
echo 2. Verify backend API is responding
echo 3. Check database connectivity
echo 4. Share with friends!
echo.
pause
