@echo off
REM SAKHA BOT - Configuration Verification Script (Windows)
REM This script verifies your SAKHA bot configuration

setlocal enabledelayedexpansion
color 0A
cls

echo.
echo ╔════════════════════════════════════════════════════╗
echo ║   SAKHA BOT - Configuration ^& Security Check      ║
echo ║              Windows Version                       ║
echo ╚════════════════════════════════════════════════════╝
echo.

set FILES_OK=0
set ENV_OK=0
set SECURITY_OK=0

REM Check critical files
echo 🔍 Checking Configuration Files...
echo.

if exist ".env" (
    echo ✅ Found: .env
    set /a FILES_OK+=1
) else (
    echo ❌ Missing: .env
)

if exist ".gitignore" (
    echo ✅ Found: .gitignore
    set /a FILES_OK+=1
) else (
    echo ❌ Missing: .gitignore
)

if exist "requirements.txt" (
    echo ✅ Found: requirements.txt
    set /a FILES_OK+=1
) else (
    echo ❌ Missing: requirements.txt
)

if exist "sakha\main.py" (
    echo ✅ Found: sakha\main.py
    set /a FILES_OK+=1
) else (
    echo ❌ Missing: sakha\main.py
)

echo.
echo 🔐 Checking Environment Variables...
echo.

REM Check .env contents using findstr
findstr /L "WHATSAPP_BUSINESS_ACCOUNT_ID=283437264692233" .env >nul 2>&1
if !errorlevel! equ 0 (
    echo ✅ WhatsApp Account ID configured
    set /a ENV_OK+=1
) else (
    echo ❌ WhatsApp Account ID NOT configured
)

findstr /L "OPENAI_API_KEY=sk-or-v1-c8812" .env >nul 2>&1
if !errorlevel! equ 0 (
    echo ✅ OpenAI API Key configured
    set /a ENV_OK+=1
) else (
    echo ❌ OpenAI API Key NOT configured
)

findstr /L "DEEPSEEK_API_KEY=sk-or-v1-867c" .env >nul 2>&1
if !errorlevel! equ 0 (
    echo ✅ DeepSeek API Key configured
    set /a ENV_OK+=1
) else (
    echo ❌ DeepSeek API Key NOT configured
)

findstr /L "GEMINI_API_KEY=sk-or-v1-a509" .env >nul 2>&1
if !errorlevel! equ 0 (
    echo ✅ Gemini API Key configured
    set /a ENV_OK+=1
) else (
    echo ❌ Gemini API Key NOT configured
)

findstr /L "WHATSAPP_BUSINESS_ACCESS_TOKEN=EAAVfQR8" .env >nul 2>&1
if !errorlevel! equ 0 (
    echo ✅ WhatsApp Access Token configured
    set /a ENV_OK+=1
) else (
    echo ❌ WhatsApp Access Token NOT configured
)

echo.
echo 🛡️  Checking Security...
echo.

REM Check .gitignore
findstr /L "^\.env$" .gitignore >nul 2>&1
if !errorlevel! equ 0 (
    echo ✅ .env properly ignored in git
    set /a SECURITY_OK+=1
) else (
    echo ❌ .env NOT properly ignored
)

findstr "\.env\." .gitignore >nul 2>&1
if !errorlevel! equ 0 (
    echo ✅ Environment variants ignored
    set /a SECURITY_OK+=1
) else (
    echo ⚠️  Consider ignoring .env variants
)

findstr "whatsapp_auth" .gitignore >nul 2>&1
if !errorlevel! equ 0 (
    echo ✅ WhatsApp auth files ignored
    set /a SECURITY_OK+=1
) else (
    echo ❌ WhatsApp auth NOT ignored
)

echo.
echo 📊 Configuration Summary
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

echo Configuration Files: %FILES_OK%/4
echo Environment Variables: %ENV_OK%/5
echo Security Checks: %SECURITY_OK%/3

echo.
echo.

if %FILES_OK% equ 4 if %ENV_OK% equ 5 if %SECURITY_OK% equ 3 (
    color 0B
    echo ✅ All checks passed! Ready for deployment.
    echo.
    echo Next steps:
    echo   1. python run.py              # Test locally
    echo   2. docker-compose up -d       # Or deploy with Docker
    echo   3. Deploy to Railway/Render   # Or cloud platform
    echo.
    pause
    exit /b 0
) else (
    color 0C
    echo ⚠️  Some checks failed. Please review above.
    echo.
    echo Common issues:
    echo   - Missing .env file: Copy .env.example to .env
    echo   - Missing credentials: Add API keys to .env
    echo   - Missing .gitignore: Create from template
    echo.
    pause
    exit /b 1
)
