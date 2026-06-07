#!/bin/bash
# SAKHA BOT - Verification & Setup Script
# This script verifies your configuration and prepares for deployment

set -e

echo "╔════════════════════════════════════════════════════╗"
echo "║   SAKHA BOT - Configuration & Security Check      ║"
echo "╚════════════════════════════════════════════════════╝"
echo ""

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check function
check_file() {
    if [ -f "$1" ]; then
        echo -e "${GREEN}✅${NC} Found: $1"
        return 0
    else
        echo -e "${RED}❌${NC} Missing: $1"
        return 1
    fi
}

check_contains() {
    if grep -q "$2" "$1" 2>/dev/null; then
        echo -e "${GREEN}✅${NC} $3"
        return 0
    else
        echo -e "${RED}❌${NC} $3 NOT FOUND"
        return 1
    fi
}

echo "🔍 Checking Configuration Files..."
echo ""

# Check critical files
FILES_OK=0
check_file ".env" && ((FILES_OK++))
check_file ".gitignore" && ((FILES_OK++))
check_file "requirements.txt" && ((FILES_OK++))
check_file "sakha/main.py" && ((FILES_OK++))

echo ""
echo "🔐 Checking Environment Variables..."
echo ""

# Check .env contents
ENV_OK=0
check_contains ".env" "WHATSAPP_BUSINESS_ACCOUNT_ID=283437264692233" "WhatsApp Account ID" && ((ENV_OK++))
check_contains ".env" "WHATSAPP_BUSINESS_PHONE_NUMBER_ID=120924347560027" "WhatsApp Phone ID" && ((ENV_OK++))
check_contains ".env" "OPENAI_API_KEY=sk-or-v1-c8812" "OpenAI API Key (Primary)" && ((ENV_OK++))
check_contains ".env" "DEEPSEEK_API_KEY=sk-or-v1-867c" "DeepSeek API Key (Primary)" && ((ENV_OK++))
check_contains ".env" "GEMINI_API_KEY=sk-or-v1-a509" "Gemini API Key (Primary)" && ((ENV_OK++))

echo ""
echo "🛡️ Checking Security..."
echo ""

# Check .gitignore
SECURITY_OK=0

if grep -q "^\.env$" ".gitignore" 2>/dev/null; then
    echo -e "${GREEN}✅${NC} .env properly ignored in git"
    ((SECURITY_OK++))
else
    echo -e "${RED}❌${NC} .env NOT properly ignored!"
fi

if grep -q "\.env\." ".gitignore" 2>/dev/null; then
    echo -e "${GREEN}✅${NC} Environment variants ignored"
    ((SECURITY_OK++))
else
    echo -e "${YELLOW}⚠️${NC} Consider ignoring .env variants"
fi

# Check if .env is not in git
if git ls-files --error-unmatch .env >/dev/null 2>&1; then
    echo -e "${RED}❌${NC} WARNING: .env is tracked by git!"
    echo "    Run: git rm --cached .env"
else
    echo -e "${GREEN}✅${NC} .env is not tracked by git"
    ((SECURITY_OK++))
fi

echo ""
echo "📊 Configuration Summary"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Summary
echo "Configuration Files: $FILES_OK/4"
echo "Environment Variables: $ENV_OK/5"
echo "Security Checks: $SECURITY_OK/3"

echo ""

# Overall status
if [ $FILES_OK -eq 4 ] && [ $ENV_OK -eq 5 ] && [ $SECURITY_OK -eq 3 ]; then
    echo -e "${GREEN}✅ All checks passed! Ready for deployment.${NC}"
    echo ""
    echo "Next steps:"
    echo "  1. python run.py              # Test locally"
    echo "  2. docker-compose up -d       # Or deploy with Docker"
    echo "  3. Deploy to Railway/Render   # Or cloud platform"
    exit 0
else
    echo -e "${YELLOW}⚠️ Some checks failed. Please review above.${NC}"
    echo ""
    echo "Common issues:"
    echo "  - Missing .env file: Copy .env.example to .env"
    echo "  - Missing credentials: Add API keys to .env"
    echo "  - .env tracked in git: Run 'git rm --cached .env'"
    exit 1
fi
