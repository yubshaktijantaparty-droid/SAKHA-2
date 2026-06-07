# SAKHA AI - Deployment Guide

## Deployment Options

### Option 1: Railway (Recommended)

**Advantages:**
- Simple deployment
- Automatic scaling
- Built-in monitoring
- Free tier available

**Steps:**

1. **Create Railway Account**
   - Go to railway.app
   - Sign up with GitHub

2. **Connect Repository**
   - Connect your GitHub repo
   - Railway auto-detects Python/Node.js

3. **Set Environment Variables**
   ```
   MONGODB_URI=your-mongodb-uri
   OPENAI_API_KEY=sk-...
   DEEPSEEK_API_KEY=sk-...
   GEMINI_API_KEY=sk-...
   DEFAULT_AI_PROVIDER=openai
   ENVIRONMENT=production
   DEBUG_MODE=false
   ```

4. **Deploy**
   - Railway automatically deploys on push
   - Check deployment logs in dashboard

### Option 2: Render

**Steps:**

1. Create new Web Service on render.com
2. Connect GitHub repository
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `python backend/run.py`
5. Add environment variables
6. Deploy

### Option 3: Docker (Self-Hosted)

**Build:**
```bash
docker build -t sakha-ai:latest .
```

**Run:**
```bash
docker-compose up -d
```

**For production:**
```bash
docker run -d \
  --name sakha-ai \
  -p 8000:8000 \
  -e MONGODB_URI=mongodb://... \
  -e OPENAI_API_KEY=sk-... \
  sakha-ai:latest
```

## Frontend Deployment

### GitHub Pages

1. **Update vite.config.ts**
   ```typescript
   export default {
     base: '/sakha-ai/',  // if repo name is sakha-ai
   }
   ```

2. **Build**
   ```bash
   npm run build
   ```

3. **Deploy**
   ```bash
   npm run deploy  # uses gh-pages package
   ```

### Vercel

1. Connect GitHub repo to Vercel
2. Set environment variables
3. Deploy (automatic on push)

### Netlify

```bash
npm run build
# Deploy /dist folder to Netlify
```

## Backend API Deployment

### Health Checks

Railway/Render automatically checks `/api/health` endpoint.

### Environment Variables Required

```env
# Required
MONGODB_URI=
OPENAI_API_KEY=
DEFAULT_AI_PROVIDER=openai
SECRET_KEY=generate-random-key
JWT_SECRET=generate-random-key

# Optional
DEEPSEEK_API_KEY=
GEMINI_API_KEY=
STABILITY_AI_API_KEY=
```

### Database Setup

MongoDB connection:
```
mongodb+srv://user:password@cluster.mongodb.net/sakha_db
```

## Performance Optimization

### Frontend
```bash
# Analyze bundle size
npm run build -- --stats

# Lazy load routes
React.lazy(() => import('./pages/ImageGenerator'))
```

### Backend
```python
# Enable caching
from functools import lru_cache

# Use connection pooling
MONGODB_URI includes connection pool settings
```

## Monitoring & Logging

### Sentry Integration

```python
import sentry_sdk
sentry_sdk.init("your-sentry-dsn")
```

### CloudFlare Analytics

1. Add Cloudflare between domain and app
2. Enable analytics
3. Monitor traffic and performance

## SSL/HTTPS

Railway/Render automatically provide SSL certificates.

For custom domains:
- Use Cloudflare (free)
- Use Let's Encrypt
- AWS Certificate Manager

## CI/CD Pipeline

### GitHub Actions

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: 18
      - uses: actions/setup-python@v4
        with:
          python-version: "3.10"
      
      - name: Build frontend
        run: cd frontend && npm install && npm run build
      
      - name: Test backend
        run: cd backend && pip install -r requirements.txt && pytest
      
      - name: Deploy to Railway
        run: railway deploy
        env:
          RAILWAY_TOKEN: ${{ secrets.RAILWAY_TOKEN }}
```

## Rollback

### Railway
- Click "Rollback" in deployment history

### Docker
```bash
docker pull sakha-ai:v1.0
docker run -d sakha-ai:v1.0
```

## Security Checklist

- [ ] API keys stored in environment variables
- [ ] CORS properly configured
- [ ] Rate limiting enabled
- [ ] SSL/HTTPS enabled
- [ ] Database backed up daily
- [ ] Admin panel protected
- [ ] Input validation on all endpoints
- [ ] Error messages don't leak sensitive info

## Cost Estimation

| Service | Plan | Cost |
|---------|------|------|
| Railway | Starter | $5/month |
| MongoDB Atlas | Shared | Free - $57/month |
| OpenAI API | Pay-as-you-go | Varies |
| Cloudflare | Free | Free |
| **Total** | | ~$100-200/month |

## Troubleshooting

### Backend not starting
```bash
# Check logs
railway logs

# Test locally
python backend/run.py --debug
```

### Frontend not loading
```bash
# Check API URL in vite.config.ts
# Check CORS settings in backend
```

### Database connection errors
```bash
# Verify MongoDB URI
# Check IP whitelist in MongoDB Atlas
# Verify database exists
```

## Support

- Railway Support: https://docs.railway.app
- FastAPI Docs: https://fastapi.tiangolo.com
- Vite Docs: https://vitejs.dev
