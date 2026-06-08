# SAKHA AI - Complete GitHub + Railway Deployment

## Architecture
```
GitHub (Frontend + Backend Code)
    ↓
Railway (Backend API)
    ↓
MongoDB Atlas (Database)
    ↓
GitHub Pages (Frontend Static Files)
```

---

## Step 1: Deploy Backend to Railway

### 1.1 Create Railway Project
1. Go to https://railway.app
2. Create new account (or login)
3. Click "Create New Project"
4. Select "Deploy from GitHub repo"
5. Select: `yubshaktijantaparty-droid/SAKHA-2`

### 1.2 Configure Environment Variables
In Railway, go to **Project Settings** → **Variables**:

```
ENVIRONMENT=production
DEBUG_MODE=false
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/sakha_premium_db
SECRET_KEY=<generate-32-character-random-string>
JWT_SECRET=<generate-32-character-random-string>
OPENROUTER_OWL_ALPHA_API_KEY=sk-or-v1-xxxxx
OPENROUTER_PREMIUM_API_KEY=sk-or-v1-xxxxx
CORS_ORIGINS=https://yubshaktijantaparty-droid.github.io,http://localhost:5173
```

**How to generate random strings (PowerShell):**
```powershell
# Generate random 32-char string
[Convert]::ToBase64String([System.Security.Cryptography.RNGCryptoServiceProvider]::new().GetBytes(32))
```

### 1.3 Wait for Deployment
- Railway auto-deploys from GitHub
- Watch deployment logs
- Look for: "Application startup complete"
- Copy your service URL (looks like: `https://sakha-production-xxxx.railway.app`)

---

## Step 2: Get MongoDB Connection String

### Option A: Use Railway MongoDB (Simplest)
1. In Railway project, click "Add Service"
2. Select "MongoDB"
3. Railway creates it and injects `MONGODB_URI` automatically
4. **Skip to Step 3**

### Option B: Use MongoDB Atlas (More Control)
1. Go to https://www.mongodb.com/cloud/atlas
2. Create free account
3. Create free cluster
4. Get connection string:
   ```
   mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/sakha_premium_db?retryWrites=true&w=majority
   ```
5. Add to Railway variables as `MONGODB_URI`

---

## Step 3: Update Frontend with Backend URL

### 3.1 Get Your Railway URL
From Railway dashboard:
1. Go to Deployments tab
2. Find your service
3. Copy the public domain URL (e.g., `https://sakha-production-xyz.railway.app`)

### 3.2 Update Build Script
Edit `frontend/package.json`:
```json
"scripts": {
  "build:railway": "cross-env VITE_REPO_NAME=SAKHA-2 VITE_API_URL=https://your-railway-url npm run build:prod"
}
```

Replace `https://your-railway-url` with your actual Railway domain.

### 3.3 Build and Deploy
```bash
cd frontend

# Build with Railway API URL
npm run build:railway

# Copy to GitHub Pages deployment folder
Copy-Item -Path "dist/*" -Destination "../docs" -Recurse -Force

cd ..

# Commit and push
git add .
git commit -m "Deploy: Connect frontend to Railway backend"
git push
```

---

## Step 4: Test Complete Workflow

### 4.1 Test Backend Directly
```
https://your-railway-url/api/docs
```
- You should see Swagger UI
- Try the `/api/chat/models` endpoint

### 4.2 Test Frontend on GitHub Pages
1. Visit: https://yubshaktijantaparty-droid.github.io/SAKHA-2/
2. Click "Start Chatting"
3. Enter any email and password (6+ chars)
4. Click "Sign In"
5. Select an AI model from dropdown
6. Send a message: "What is quantum computing?"
7. **✅ You should see real AI response!**

### 4.3 Check Models Display
- Open DevTools (F12)
- Network tab
- Look for `/api/chat/models` call
- Should show multiple AI models

---

## Troubleshooting

### Models Not Loading
**Problem**: Dropdown only shows one model or empty
**Solutions**:
1. Check Railway logs for API errors
2. Verify OpenRouter API key is valid
3. Check browser console for network errors
4. Verify VITE_API_URL is set correctly

### Login Fails
**Problem**: "Cannot reach backend"
**Solutions**:
1. Verify Railway backend is running (check Deployments)
2. Check CORS_ORIGINS includes GitHub Pages domain
3. Verify MongoDB connection string is correct
4. Check Railway logs for connection errors

### API Timeout
**Problem**: "Request timeout"
**Solutions**:
1. Wait 30-60 seconds (Railway cold start)
2. Check Railway server resources
3. Check OpenRouter API rate limits
4. Try simpler query first

---

## Monitoring & Maintenance

### Railway Dashboard
- **Deployments** tab: See deployment status
- **Logs** tab: Debug errors
- **Metrics** tab: Monitor CPU, memory
- **Usage** tab: Check free tier credits

### Cost Monitoring
- Railway shows real-time usage
- Free tier: $5/month credit
- Most hobby projects use < $2/month

### Update Workflow
```bash
# Make changes locally
git add .
git commit -m "Feature: description"
git push

# Railway auto-deploys from GitHub
# Frontend rebuilds on next push to GitHub Pages
```

---

## Environment Variables Reference

| Variable | Purpose | Example |
|----------|---------|---------|
| `ENVIRONMENT` | dev/production | production |
| `DEBUG_MODE` | Enable debug logs | false |
| `MONGODB_URI` | Database connection | mongodb+srv://... |
| `SECRET_KEY` | App security | random-32-chars |
| `JWT_SECRET` | Token signing | random-32-chars |
| `OPENROUTER_*_API_KEY` | AI model access | sk-or-v1-... |
| `CORS_ORIGINS` | Allowed domains | https://your-domain |

---

## Security Checklist

- [ ] Never commit API keys to GitHub
- [ ] Use Railway's variable system for secrets
- [ ] Enable HTTPS (Railway does automatically)
- [ ] Restrict CORS_ORIGINS to your domains
- [ ] Use strong SECRET_KEY and JWT_SECRET
- [ ] Rotate API keys monthly
- [ ] Monitor Railway logs for suspicious activity

---

## File Reference

**Configuration Files Created:**
- `Procfile` - Railway startup command
- `railway.json` - Railway configuration
- `Dockerfile` - Container build steps
- `.env.railway` - Environment template
- `RAILWAY_DEPLOYMENT_GUIDE.md` - This guide

**Updated Files:**
- `frontend/package.json` - New build:railway script
- `frontend/src/services/api.ts` - Uses VITE_API_URL

---

## Quick Reference URLs

- **Railway Dashboard**: https://railway.app/dashboard
- **GitHub Repository**: https://github.com/yubshaktijantaparty-droid/SAKHA-2
- **GitHub Pages URL**: https://yubshaktijantaparty-droid.github.io/SAKHA-2/
- **MongoDB Atlas**: https://www.mongodb.com/cloud/atlas
- **OpenRouter API**: https://openrouter.ai

---

## Support

If you encounter issues:
1. Check Railway logs
2. Verify all environment variables are set
3. Test API directly: `https://your-railway-url/api/docs`
4. Check network tab in browser DevTools
5. Review this guide for common issues

**Status**: Ready for deployment! 🚀
