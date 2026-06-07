# SAKHA AI - Production Deployment Guide

Complete guide for deploying SAKHA AI to production on GitHub Pages + Render/Railway.

## 🎯 Deployment Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                  PRODUCTION SETUP                           │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  Frontend (React)      →    GitHub Pages (your-username.github.io)
│  ✓ Static files               ✓ Free hosting
│  ✓ Auto-deploy on push        ✓ SSL included
│  ✓ Custom domain support      ✓ CDN provided
│                                                               │
│  Backend (FastAPI)     →    Render or Railway
│  ✓ Dynamic API server         ✓ Auto-scaling
│  ✓ MongoDB database           ✓ Easy CI/CD
│  ✓ AI model APIs              ✓ Environment management
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

## ⚡ Quick Deploy (15 minutes)

### Step 1: Setup GitHub Repository

```bash
# Initialize git if needed
git init
git add .
git commit -m "Initial commit"

# Create repo on GitHub and push
git remote add origin https://github.com/YOUR_USERNAME/sakha-ai.git
git branch -M main
git push -u origin main
```

### Step 2: Deploy Frontend to GitHub Pages

```bash
# Install gh-pages package
cd frontend
npm install gh-pages --save-dev
```

Add to `frontend/package.json`:
```json
{
  "scripts": {
    "deploy": "vite build && gh-pages -d dist"
  },
  "homepage": "https://YOUR_USERNAME.github.io/sakha-ai"
}
```

Update `frontend/vite.config.ts`:
```typescript
export default defineConfig({
  base: '/sakha-ai/',  // Your repo name
  // ... rest of config
})
```

```bash
# Deploy
npm run deploy
```

✓ Frontend now live at: `https://YOUR_USERNAME.github.io/sakha-ai`

### Step 3: Deploy Backend to Render

**Option A: Using Render (Recommended for free tier)**

1. Go to [render.com](https://render.com)
2. Sign up with GitHub
3. Create New → Web Service
4. Connect your GitHub repository
5. Set configuration:
   - **Name**: sakha-ai-backend
   - **Environment**: Python 3.10
   - **Build Command**: `pip install -r backend/requirements.txt`
   - **Start Command**: `cd backend && python run.py`
   - **Instance Type**: Free

6. Add Environment Variables:
   - `MONGODB_URI`: Your MongoDB connection string
   - `OPENAI_API_KEY`: Your OpenAI API key
   - `DEEPSEEK_API_KEY`: Your DeepSeek API key (optional)
   - `GEMINI_API_KEY`: Your Gemini API key (optional)
   - `SUPABASE_URL`: Your Supabase URL
   - `SUPABASE_PUBLISHABLE_KEY`: Your Supabase key
   - `CORS_ORIGINS`: Add your GitHub Pages URL
   - `ENVIRONMENT`: `production`
   - `DEBUG_MODE`: `false`

7. Deploy! (Takes 5-10 minutes)

**Option B: Using Railway**

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Link project
railway link

# Deploy
railway up
```

### Step 4: Connect Frontend to Backend

Update `frontend/src/lib/supabase.ts` with your backend URL:

```typescript
const API_URL = "https://sakha-ai-backend.onrender.com"  // Your Render URL
```

Or set via environment in GitHub Actions (see CI/CD section below).

### Step 5: Setup GitHub Actions (Auto Deploy)

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to GitHub Pages & Render

on:
  push:
    branches: [ main ]

jobs:
  deploy-frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      
      - name: Install dependencies
        run: cd frontend && npm install
      
      - name: Build
        run: cd frontend && npm run build
        env:
          VITE_API_URL: ${{ secrets.VITE_API_URL }}
          VITE_REPO_NAME: sakha-ai
      
      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./frontend/dist

  deploy-backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Trigger Render Deploy
        run: |
          curl https://api.render.com/deploy/srv-${{ secrets.RENDER_SERVICE_ID }}?key=${{ secrets.RENDER_DEPLOY_KEY }}
```

### Step 6: Configure GitHub Secrets

Go to Settings → Secrets and variables → Actions

Add these secrets:
- `VITE_API_URL`: `https://sakha-ai-backend.onrender.com`
- `RENDER_SERVICE_ID`: From Render dashboard
- `RENDER_DEPLOY_KEY`: From Render dashboard
- `GITHUB_TOKEN`: Already available

## 🗄️ Database Setup

### MongoDB Atlas (Recommended)

1. Go to [mongodb.com/cloud/atlas](https://www.mongodb.com/cloud/atlas)
2. Create free account
3. Create cluster (Free tier M0)
4. Get connection string:
   ```
   mongodb+srv://username:password@cluster.mongodb.net/sakha_db?retryWrites=true&w=majority
   ```
5. Add this to `.env` as `MONGODB_URI`

### Supabase (Authentication)

1. Go to [supabase.com](https://supabase.com)
2. Create new project
3. Get credentials from Settings
4. Add to `.env`:
   - `SUPABASE_URL`
   - `SUPABASE_PUBLISHABLE_KEY`
   - `SUPABASE_SERVICE_ROLE_KEY`

## 🔑 API Keys Setup

### OpenAI
1. Go to [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. Create new API key
3. Add to environment: `OPENAI_API_KEY`

### Google Gemini
1. Go to [ai.google.dev](https://ai.google.dev)
2. Get API key from Google AI Studio
3. Add to environment: `GEMINI_API_KEY`

### DeepSeek
1. Sign up at [deepseek.com](https://deepseek.com)
2. Create API key
3. Add to environment: `DEEPSEEK_API_KEY`

## ✅ Production Checklist

- [ ] `.env` file is in `.gitignore` (no credentials in repo)
- [ ] All environment variables set in Render/Railway
- [ ] MongoDB Atlas cluster created and connection string configured
- [ ] Supabase project created with authentication enabled
- [ ] At least one AI API key configured
- [ ] CORS origins include your GitHub Pages URL
- [ ] `DEBUG_MODE=false` in production
- [ ] `ENVIRONMENT=production` set
- [ ] Deployed frontend working at GitHub Pages URL
- [ ] Deployed backend responding to API requests
- [ ] Chat messages persist in MongoDB
- [ ] User authentication working with Supabase
- [ ] Domain name configured (optional)

## 🔒 Security in Production

1. **Secrets Management**
   - All API keys in environment variables only
   - Use GitHub Secrets for CI/CD
   - Never commit `.env` files

2. **CORS Configuration**
   - Only allow your frontend URL
   - Remove localhost URLs

3. **Database Security**
   - MongoDB IP whitelist configured
   - Supabase RLS policies enabled
   - Strong passwords used

4. **Rate Limiting**
   - Enabled on backend
   - API throttling configured

## 📊 Monitoring

### Logs
- **Frontend**: Check GitHub Actions logs
- **Backend**: View in Render/Railway dashboard

### Health Check
```bash
curl https://your-backend-url/api/health
```

Should return:
```json
{
  "status": "healthy",
  "database": "connected",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

## 🆘 Troubleshooting

### Frontend not loading
- Check GitHub Pages settings (Settings → Pages → Source should be gh-pages)
- Verify `base` in `vite.config.ts` matches repo name

### Backend 502 errors
- Check Render logs for errors
- Verify all environment variables are set
- Ensure MongoDB connection string is correct

### Chat not persisting
- Verify MongoDB `MONGODB_URI` is correct
- Check MongoDB Atlas has data (check Atlas dashboard)
- Verify backend logs for database errors

### CORS errors
- Add your frontend URL to `CORS_ORIGINS` in backend
- Ensure no trailing slashes

### Images not generating
- Verify API key for image service is set
- Check that provider (Stability AI, HF, Replicate) is working
- Images fall back to placeholder if provider is unavailable

## 📈 Performance Tips

1. **Frontend**
   - Enable Vite caching
   - Use React lazy loading
   - Optimize images

2. **Backend**
   - Enable database indexing (already done)
   - Use connection pooling
   - Cache AI responses

3. **Database**
   - Regular backups
   - Monitor query performance
   - Archive old chats

## 🎉 Success!

Your SAKHA AI is now live in production! 🚀

- **Frontend**: https://YOUR_USERNAME.github.io/sakha-ai
- **Backend**: https://sakha-ai-backend.onrender.com
- **API Docs**: https://sakha-ai-backend.onrender.com/api/docs

---

**Next Steps:**
1. Share with friends!
2. Collect feedback
3. Add custom domain (optional)
4. Monitor analytics
5. Plan feature upgrades
