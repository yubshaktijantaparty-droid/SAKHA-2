# SAKHA Bot - Complete Setup Guide

## 📋 Table of Contents
1. [Prerequisites](#prerequisites)
2. [Local Development](#local-development)
3. [Database Setup](#database-setup)
4. [AI Service Configuration](#ai-service-configuration)
5. [WhatsApp Integration](#whatsapp-integration)
6. [Docker Deployment](#docker-deployment)
7. [Cloud Deployment](#cloud-deployment)
8. [Monitoring & Maintenance](#monitoring--maintenance)

---

## Prerequisites

### System Requirements
- Python 3.12 or higher
- Git
- Docker & Docker Compose (optional)
- 2GB RAM minimum
- Stable internet connection

### Required Accounts
- MongoDB Atlas (or local MongoDB)
- OpenAI Account
- WhatsApp Business Account
- GitHub (for deployment)

---

## Local Development

### 1. Clone Repository
```bash
git clone https://github.com/pranabg/sakha.git
cd sakha
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3.12 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup Environment Variables
```bash
# Copy example env
cp .env.example .env

# Edit .env with your values
nano .env  # or use your editor
```

### 5. Start Local Server
```bash
uvicorn sakha.main:app --reload --port 8000
```

Access at: http://localhost:8000

---

## Database Setup

### MongoDB Atlas (Recommended)

1. **Create Account**
   - Visit https://www.mongodb.com/cloud/atlas
   - Sign up for free tier

2. **Create Cluster**
   - Click "Create Database"
   - Choose free tier
   - Select region close to you
   - Create cluster

3. **Create Database User**
   - Go to Security > Database Access
   - Create username & password
   - Note credentials

4. **Get Connection String**
   - Click "Connect" on cluster
   - Select "Connect your application"
   - Copy connection string
   - Add to .env as MONGODB_URI

5. **Update .env**
```env
DATABASE_TYPE=mongodb
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/sakha?retryWrites=true&w=majority
MONGODB_DB_NAME=sakha_db
```

### Local MongoDB

```bash
# macOS (Homebrew)
brew install mongodb-community
brew services start mongodb-community

# Windows (Docker)
docker run -d -p 27017:27017 --name mongodb mongo:7.0

# Linux (Ubuntu)
sudo apt-get install -y mongodb
sudo systemctl start mongodb
```

### PostgreSQL Setup (Alternative)

```bash
# Create database
createdb sakha_db

# Update .env
DATABASE_TYPE=postgresql
POSTGRESQL_URI=postgresql://user:password@localhost:5432/sakha_db
```

---

## AI Service Configuration

### OpenAI (Recommended)

1. **Get API Key**
   - Visit https://platform.openai.com/account/api-keys
   - Create new API key
   - Copy to .env

2. **Set Model**
```env
OPENAI_API_KEY=sk-your-key-here
OPENAI_MODEL=gpt-4-turbo  # or gpt-3.5-turbo for cost savings
DEFAULT_AI_PROVIDER=openai
```

3. **Test Connection**
```bash
python -c "from sakha.ai import ai_service; print('✓ OpenAI connected')"
```

### Alternative Providers

**DeepSeek:**
```env
DEEPSEEK_API_KEY=your-deepseek-key
DEFAULT_AI_PROVIDER=deepseek
```

**Google Gemini:**
```env
GEMINI_API_KEY=your-gemini-key
DEFAULT_AI_PROVIDER=gemini
```

---

## WhatsApp Integration

### Option 1: Baileys (WhatsApp Web)

```bash
# Install additional dependency
pip install whatsapp-web.js

# Configuration in .env
WHATSAPP_SESSION_NAME=SAKHA_SESSION
WHATSAPP_AUTH_PATH=./whatsapp_auth
```

### Option 2: Twilio WhatsApp API

1. **Setup Twilio Account**
   - Visit https://www.twilio.com
   - Create account
   - Get phone number

2. **Configure .env**
```env
TWILIO_ACCOUNT_SID=your-sid
TWILIO_AUTH_TOKEN=your-token
TWILIO_PHONE_NUMBER=+1234567890
```

### Option 3: WhatsApp Business API

1. **Apply for Access**
   - Visit https://www.whatsapp.com/business/api
   - Fill application form
   - Get approval

2. **Configure .env**
```env
WHATSAPP_BUSINESS_ACCOUNT_ID=your-account-id
WHATSAPP_BUSINESS_PHONE_NUMBER_ID=your-phone-id
WHATSAPP_BUSINESS_ACCESS_TOKEN=your-token
```

---

## Docker Deployment

### Build Image
```bash
docker build -t sakha:latest .
```

### Run Container
```bash
docker run -d \
  -p 8000:8000 \
  --env-file .env \
  --name sakha-bot \
  sakha:latest
```

### Docker Compose
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Verify Running
```bash
curl http://localhost:8000/health
```

---

## Cloud Deployment

### Railway

1. **Setup**
   - Go to https://railway.app
   - Create new project
   - Connect GitHub repository

2. **Add Environment Variables**
   - Add all from .env in Railway UI
   - Save

3. **Deploy**
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login & Deploy
railway login
railway link
railway up
```

4. **Get Public URL**
   - Check Railway dashboard
   - Copy generated URL

### Render

1. **Create Web Service**
   - Go to https://render.com
   - Click "New +" > "Web Service"
   - Connect GitHub repo

2. **Configure**
   - Name: sakha-bot
   - Runtime: Python 3
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn sakha.main:app --host 0.0.0.0 --port $PORT`

3. **Environment Variables**
   - Add all from .env
   - Deploy

### VPS (Ubuntu Server)

1. **Connect to VPS**
```bash
ssh root@your_vps_ip
```

2. **Install Python & Dependencies**
```bash
apt-get update
apt-get install -y python3.12 python3.12-venv python3-pip
apt-get install -y git curl
```

3. **Clone Repository**
```bash
cd /opt
git clone https://github.com/pranabg/sakha.git
cd sakha
```

4. **Setup Virtual Environment**
```bash
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

5. **Create Systemd Service**
```bash
sudo nano /etc/systemd/system/sakha.service
```

Paste:
```ini
[Unit]
Description=SAKHA Bot
After=network.target

[Service]
Type=notify
User=root
WorkingDirectory=/opt/sakha
Environment="PATH=/opt/sakha/venv/bin"
ExecStart=/opt/sakha/venv/bin/uvicorn sakha.main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

6. **Enable & Start Service**
```bash
sudo systemctl enable sakha
sudo systemctl start sakha
sudo systemctl status sakha
```

7. **Setup Nginx Reverse Proxy**
```bash
sudo apt-get install -y nginx

sudo nano /etc/nginx/sites-available/sakha
```

Paste:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

Enable:
```bash
sudo ln -s /etc/nginx/sites-available/sakha /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

## Monitoring & Maintenance

### View Logs
```bash
# Local
tail -f logs/sakha.log

# Docker
docker-compose logs -f sakha-bot

# VPS
sudo journalctl -u sakha -f
```

### Health Check
```bash
curl http://localhost:8000/health
```

### Database Backup

**MongoDB:**
```bash
mongodump --uri="mongodb+srv://..." --out=./backups
```

**Automatic Backup (Docker):**
```bash
# Add to docker-compose.yml
volumes:
  - ./backups:/backups
```

### Performance Monitoring

```bash
# Check system resources
watch -n 1 'docker stats'

# Monitor API responses
curl -w "@curl-format.txt" http://localhost:8000/health
```

### Updates

```bash
# Pull latest code
git pull origin main

# Install new dependencies
pip install -r requirements.txt

# Restart services
docker-compose restart

# Or on VPS
sudo systemctl restart sakha
```

---

## Troubleshooting

### Database Connection Fails
```bash
# Test MongoDB connection
python -c "from pymongo import MongoClient; MongoClient('your-uri').admin.command('ping')"

# Check VPC/Network access
# Ensure IP is whitelisted in MongoDB Atlas
```

### API Not Responding
```bash
# Check if service is running
docker ps
systemctl status sakha

# Check logs for errors
docker logs sakha-bot
```

### WhatsApp Not Working
- Verify webhook URL is public
- Check WhatsApp Business Account status
- Verify API credentials
- Test webhook with sample payload

### High Response Time
- Check database performance
- Increase resource allocation
- Optimize database queries
- Add caching layer (Redis)

---

## Next Steps

1. ✅ Deploy to production
2. ✅ Configure WhatsApp webhook
3. ✅ Set up monitoring
4. ✅ Create backup strategy
5. ✅ Document API endpoints
6. ✅ Setup CI/CD pipeline

---

**For support: contact@example.com**
