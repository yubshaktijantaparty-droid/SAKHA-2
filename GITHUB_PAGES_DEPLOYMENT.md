# GitHub Pages + Render Deployment Guide

Deploy your SAKHA AI application to **GitHub Pages (Frontend)** + **Render (Backend)** in 15 minutes.

## 📋 Prerequisites

- GitHub account with a new repository
- Render account (free tier available)
- API keys (OpenAI, DeepSeek, or Gemini)
- MongoDB Atlas account (free tier available)

---

## 🚀 Step 1: Prepare Your Repository

### 1.1 Create GitHub Repository

```bash
# Option A: New Repository
1. Go to https://github.com/new
2. Repository name: sakha-ai (or your preferred name)
3. Description: Premium AI ChatGPT-like Website
4. Public repository
5. Initialize with README
6. Click "Create repository"
```

### 1.2 Push Your Code to GitHub

```bash
cd /path/to/sakha-ai

# If not initialized yet
git init
git add .
git commit -m "Initial commit: SAKHA AI ChatGPT website"

# Add remote (replace YOUR_USERNAME and REPO_NAME)
git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git
git branch -M main
git push -u origin main
```

---

## 🔧 Step 2: Setup Render Backend

### 2.1 Create Render Account

1. Go to [render.com](https://render.com)
2. Sign up with GitHub (recommended)
3. Create new account and verify email

### 2.2 Deploy Backend Service

1. In Render dashboard, click **"New +"** → **"Web Service"**
2. Connect GitHub repository
3. Fill in deployment details:
   - **Name:** sakha-backend
   - **Runtime:** Python 3.10
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `cd backend && python run.py`
   - **Region:** Choose closest to you

### 2.3 Configure Environment Variables

In Render dashboard → sakha-backend → Environment:

```env
SERVER_HOST=0.0.0.0
SERVER_PORT=8000
ENVIRONMENT=production
DEBUG_MODE=False

# AI Services
OPENAI_API_KEY=sk-your-key
DEEPSEEK_API_KEY=sk-your-key
GEMINI_API_KEY=your-key
DEFAULT_AI_PROVIDER=openai

# Database
MONGODB_URI=mongodb+srv://user:pass@cluster.mongodb.net/sakha_db
MONGODB_DB_NAME=sakha_db

# CORS - Update with your GitHub Pages URL
CORS_ORIGINS=https://YOUR_USERNAME.github.io
```

### 2.4 Note Your Backend URL

After deployment, you'll get a URL like:
```
https://sakha-backend-xxxx.onrender.com
```

Save this URL - you'll need it in Step 4.

---

## 🎨 Step 3: Setup GitHub Pages Frontend

### 3.1 Enable GitHub Pages

1. Go to GitHub repository → **Settings**
2. Left menu → **Pages**
3. **Build and deployment:**
   - Source: **GitHub Actions**
   - Click **Configure**

### 3.2 GitHub Secrets Configuration

1. Go to Settings → **Secrets and variables** → **Actions**
2. Create new secrets:

```
Name: VITE_API_URL
Value: https://sakha-backend-xxxx.onrender.com

Name: VITE_REPO_NAME
Value: sakha-ai (or your repo name)

Name: RENDER_SERVICE_ID
Value: (from Render dashboard URL)

Name: RENDER_DEPLOY_KEY
Value: (from Render dashboard → Settings)
```

### 3.3 Update Vite Config

File: `frontend/vite.config.ts` (Already updated ✓)

---

## 🔄 Step 4: Configure API Endpoints

### 4.1 Update Environment Files

**File: `.env.production`**

```env
VITE_API_URL=https://sakha-backend-xxxx.onrender.com
VITE_REPO_NAME=sakha-ai
```

**File: `.env.example`**

```env
# Development
VITE_API_URL=http://localhost:8000
VITE_REPO_NAME=sakha-ai

# Production (GitHub Pages + Render)
# VITE_API_URL=https://sakha-backend-xxxx.onrender.com
```

### 4.2 API Service Auto-Configuration

The API service automatically:
- Uses `/api` for local development
- Uses your `VITE_API_URL` for production
- No hardcoded URLs needed ✓

---

## 🚢 Step 5: Deploy

### 5.1 Deploy Backend

Backend auto-deploys when you push to `main` branch (configured in GitHub Actions).

```bash
# Push code to trigger deployment
git add .
git commit -m "Setup GitHub Pages + Render deployment"
git push origin main
```

Check deployment at: [render.com](https://render.com) → Dashboard

### 5.2 Deploy Frontend

Frontend auto-deploys to GitHub Pages via GitHub Actions.

**Check deployment:**
1. Go to GitHub repository → **Actions**
2. Watch workflow progress
3. Access at: `https://YOUR_USERNAME.github.io/sakha-ai/`

---

## 🎯 Step 6: Custom Domain (Optional)

### 6.1 GitHub Pages Custom Domain

1. Go to Settings → **Pages**
2. **Custom domain:** `yourdomain.com`
3. Add DNS records (shown in GitHub)
4. Wait for HTTPS certificate (5-10 mins)

### 6.2 Update Environment Variables

Update `VITE_API_URL` and `CORS_ORIGINS` in:
- GitHub Secrets
- Render Environment Variables

---

## ✅ Verification

### Backend Health Check

```bash
curl https://sakha-backend-xxxx.onrender.com/api/health
# Should return: {"status": "healthy"}
```

### Frontend Access

```
https://YOUR_USERNAME.github.io/sakha-ai/
```

### API Documentation

```
https://sakha-backend-xxxx.onrender.com/api/docs
```

---

## 📊 Deployment Architecture

```
GitHub Repository
├── Frontend (React)
│   └── Deployed to → GitHub Pages
│       URL: https://YOUR_USERNAME.github.io/sakha-ai
│
└── Backend (FastAPI)
    └── Deployed to → Render
        URL: https://sakha-backend-xxxx.onrender.com
        
Data Flow:
GitHub Pages → CORS Request → Render Backend → MongoDB Atlas
```

---

## 🔐 Security Checklist

- [ ] API keys stored in GitHub Secrets (not in code)
- [ ] CORS configured for your domain
- [ ] MongoDB URI with Atlas IP whitelist
- [ ] `.env` file in `.gitignore`
- [ ] HTTPS enabled (automatic on GitHub Pages & Render)
- [ ] Error messages don't expose sensitive info

---

## 📱 Access Points

| Component | URL | Status |
|-----------|-----|--------|
| Frontend | https://YOUR_USERNAME.github.io/sakha-ai | Auto-deployed |
| API Docs | https://sakha-backend-xxxx.onrender.com/api/docs | Available |
| Health Check | https://sakha-backend-xxxx.onrender.com/api/health | Check |
| Chat API | https://sakha-backend-xxxx.onrender.com/api/chat | Working |

---

## 🆘 Troubleshooting

### GitHub Pages shows 404

```bash
# Check:
1. Repository is PUBLIC
2. Workflow completed successfully (Actions tab)
3. Frontend folder has dist/ directory
4. VITE_REPO_NAME matches repository name
```

### Backend not responding

```bash
# Check:
1. Render service is running (Dashboard → Services)
2. Environment variables are set
3. MongoDB URI is correct
4. CORS_ORIGINS includes GitHub Pages URL
```

### CORS errors in browser console

**Solution:**
1. Check Render environment: `CORS_ORIGINS`
2. Include your GitHub Pages URL:
   ```
   https://YOUR_USERNAME.github.io
   ```
3. Redeploy backend after changing CORS

### API calls return 502 Bad Gateway

**Solution:**
1. Check backend logs: Render Dashboard → Logs
2. Verify MongoDB connection
3. Check API key validity
4. Restart service: Render Dashboard → Restart

---

## 🚀 Next Steps

1. Monitor GitHub Actions workflow
2. Check Render logs for any errors
3. Test API endpoints manually
4. Share your site: `https://YOUR_USERNAME.github.io/sakha-ai`

---

## 📚 Useful Links

- [GitHub Pages Documentation](https://docs.github.com/en/pages)
- [Render Documentation](https://render.com/docs)
- [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [Vite Documentation](https://vitejs.dev)

---

**Deployment Complete! Your SAKHA AI is now live on GitHub Pages! 🎉**

For continuous updates, just push to `main` branch and both frontend and backend will auto-deploy.
