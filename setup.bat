@echo off
REM SAKHA AI - Quick Development Start Script (Windows)

setlocal enabledelayedexpansion

cls
echo.
echo ===== SAKHA AI Quick Start (Windows) =====
echo.

REM Check Node.js
echo Checking Node.js...
where node >nul 2>nul
if %errorlevel% neq 0 (
    echo Node.js not found. Please install Node.js 18+
    pause
    exit /b 1
)
for /f "tokens=*" %%i in ('node --version') do set NODE_VERSION=%%i
echo [OK] Node.js %NODE_VERSION%
echo.

REM Check Python
echo Checking Python...
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo Python not found. Please install Python 3.10+
    pause
    exit /b 1
)
for /f "tokens=*" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo [OK] %PYTHON_VERSION%
echo.

REM Backend Setup
echo Setting up Backend...
cd backend
if not exist "venv" (
    python -m venv venv
)
call venv\Scripts\activate.bat
pip install -q -r requirements.txt
echo [OK] Backend dependencies installed
echo.

REM Frontend Setup
echo Setting up Frontend...
cd ..\frontend
call npm install -q
echo [OK] Frontend dependencies installed
echo.

echo.
echo ===== Setup Complete! =====
echo.
echo To start developing:
echo Terminal 1: cd backend ^& python run.py
echo Terminal 2: cd frontend ^& npm run dev
echo.
echo Backend API: http://localhost:8000
echo Frontend: http://localhost:5173
echo API Docs: http://localhost:8000/api/docs
echo.
pause
