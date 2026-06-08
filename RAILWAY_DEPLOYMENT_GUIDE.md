# SAKHA AI - Railway Deployment Guide

## Quick Start - Deploy in 5 Minutes

### Step 1: Create Railway Account & Project
1. Go to https://railway.app
2. Click "Start New Project"
3. Select "Deploy from GitHub"
4. Connect your GitHub account
5. Select repository: `yubshaktijantaparty-droid/SAKHA-2`

### Step 2: Configure Environment Variables
In Railway Dashboard, go to **Variables** and add:

```
ENVIRONMENT=production
DEBUG_MODE=false
MONGODB_URI=<your_mongodb_connection_string>
SECRET_KEY=<generate_random_string_32_chars>
JWT_SECRET=<generate_random_string_32_chars>
OPENROUTER_OWL_ALPHA_API_KEY=<your_api_key>
OPENROUTER_PREMIUM_API_KEY=<your_api_key>
CORS_ORIGINS=https://yubshaktijantaparty-droid.github.io,http://localhost:5173
```

### Step 3: Add MongoDB (If not using external Atlas)
1. Click "Add Service"
2. Select "MongoDB"
3. Railway will create and inject `MONGODB_URI` automatically

### Step 4: Deploy
1. Railway auto-deploys from GitHub pushes
2. Watch the deployment logs
3. Get your service URL from Railway dashboard

### Step 5: Update Frontend API URL
Update build environment in `package.json`:
```bash
"build:prod": "cross-env VITE_REPO_NAME=SAKHA-2 VITE_API_URL=https://your-railway-app.railway.app npm run build"
```

Then:
```bash
npm run build:prod
git add .
git commit -m "Update API URL to Railway backend"
git push
```

---

## Environment Variables Explained

| Variable | Description | Example |
|----------|-------------|---------|
| `ENVIRONMENT` | dev/production | production |
| `MONGODB_URI` | Database connection | mongodb+srv://... |
| `SECRET_KEY` | Security key | random 32 chars |
| `JWT_SECRET` | JWT signing key | random 32 chars |
| `OPENROUTER_OWL_ALPHA_API_KEY` | AI API key | sk-or-v1-... |
| `CORS_ORIGINS` | Allowed domains | https://your-domain.com |

---

## Generate Secure Keys

```bash
# Linux/Mac
openssl rand -hex 16

# PowerShell (Windows)
[Convert]::ToBase64String((1..32 | ForEach-Object {Get-Random -Maximum 256}))
```

---

## MongoDB Setup Options

### Option A: Railway MongoDB (Free)
- Click "Add Service" → "MongoDB"
- Railway handles everything automatically

### Option B: MongoDB Atlas (Free Cloud)
1. Go to https://www.mongodb.com/cloud/atlas
2. Create account → Create free cluster
3. Get connection string: `mongodb+srv://username:password@cluster.mongodb.net/sakha_premium_db`
4. Add to Railway variables as `MONGODB_URI`

---

## Deploy & Test

1. **Check Railway Logs**
   - Railway dashboard → Logs tab
   - Look for "Application startup complete"

2. **Get Your Service URL**
   - Railway dashboard → Deployments tab
   - Find your domain (looks like: `https://sakha-ai-production-xxxx.railway.app`)

3. **Test Backend**
   ```
   https://your-railway-url/api/docs
   ```

4. **Update Frontend & Rebuild**
   ```bash
   VITE_API_URL=https://your-railway-url npm run build:prod
   git push
   ```

5. **Test on GitHub Pages**
   - Visit: https://yubshaktijantaparty-droid.github.io/SAKHA-2/
   - Login → Chat → Send message → Get AI response ✓

---

## Troubleshooting

### Service Not Starting
- Check logs for errors
- Verify `MONGODB_URI` is correct
- Ensure `requirements.txt` has all dependencies

### API Calls Failing
- Check CORS_ORIGINS variable
- Verify API URL in frontend
- Check Railway logs for API errors

### Models Not Loading
- Verify OpenRouter API key is valid
- Check network tab in browser DevTools
- Ensure backend is responding with `/api/chat/models`

---

## Production Checklist

- [ ] MongoDB Atlas set up with backup
- [ ] All API keys configured in Railway
- [ ] CORS_ORIGINS includes your GitHub Pages domain
- [ ] Frontend rebuilt with correct VITE_API_URL
- [ ] Tested complete workflow (login → chat → response)
- [ ] SSL certificate enabled (Railway handles automatically)
- [ ] Monitoring/logs enabled

---

## Cost

**Railway Free Tier Includes:**
- $5/month free credits
- Perfect for hobby projects
- Upgrade to Pro if needed (~$7/month)

**Total Monthly Cost:**
- Frontend: $0 (GitHub Pages free)
- Backend: $0-5 (Railway)
- Database: $0 (Railway free tier)
- **Total: FREE**

---

## Support & Docs

- Railway Docs: https://docs.railway.app
- FastAPI Docs: https://fastapi.tiangolo.com
- OpenRouter: https://openrouter.ai

---

**Status**: Ready to deploy!
