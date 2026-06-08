# 🚀 DEPLOY TO RAILWAY - QUICK START

## Your Goal: Get Real AI Responses on GitHub Pages

**Status**: ✅ All code ready  
**Time to deploy**: 15 minutes  
**Cost**: Free ($5/month credits on Railway)

---

## STEP 1️⃣ : Setup Railway Backend

### 1. Go to Railway.app
```
https://railway.app
```

### 2. Create Account (Free)
- Sign up with GitHub or email
- Connect your GitHub account

### 3. New Project
1. Click "Create New Project"
2. Select "Deploy from GitHub repo"
3. Select: **yubshaktijantaparty-droid/SAKHA-2**
4. Click "Deploy"

### 4. Wait for Deployment
- Railway automatically deploys code from GitHub
- Check **Deployments** tab
- Wait for: "Build successful" ✅

---

## STEP 2️⃣ : Add MongoDB

### In Railway Dashboard:
1. Click "Add Service"
2. Select "**MongoDB**"
3. Railway automatically configures it
4. **Done!** MongoDB connection string is auto-injected

**Alternative**: Use MongoDB Atlas (optional, more control)
- Go to: https://www.mongodb.com/cloud/atlas
- Create free cluster
- Get connection string
- Add as `MONGODB_URI` variable in Railway

---

## STEP 3️⃣ : Add API Keys to Railway

### In Railway Project Settings → Variables:

Add these variables (click the pencil icon):

```
ENVIRONMENT = production
DEBUG_MODE = false
OPENROUTER_OWL_ALPHA_API_KEY = your_key_here
OPENROUTER_PREMIUM_API_KEY = your_key_here
SECRET_KEY = generate_random_32_chars
JWT_SECRET = generate_random_32_chars
CORS_ORIGINS = https://yubshaktijantaparty-droid.github.io
```

**Where to get keys:**
- OpenRouter: https://openrouter.ai → Get API key
- Generate random strings (PowerShell):
  ```powershell
  [Convert]::ToBase64String([System.Security.Cryptography.RNGCryptoServiceProvider]::new().GetBytes(32))
  ```

---

## STEP 4️⃣ : Get Your Railway URL

### In Railway Dashboard:
1. Go to **Deployments** tab
2. Find your service
3. Copy the domain (looks like):
   ```
   https://sakha-ai-prod-xyz123.railway.app
   ```
4. **Save this URL** - you'll need it in Step 5

---

## STEP 5️⃣ : Update Frontend with Railway URL

### On Your Local Computer:

```bash
# Open frontend package.json and update the build:railway line
# Replace: https://your-railway-url
# With: your actual Railway URL from Step 4

cd "c:\Users\prana\OneDrive\Desktop\Sakha 2\frontend"
```

### Edit `package.json` Line 9:
```json
"build:railway": "cross-env VITE_REPO_NAME=SAKHA-2 VITE_API_URL=https://your-railway-url npm run build:prod"
```

**Example:**
```json
"build:railway": "cross-env VITE_REPO_NAME=SAKHA-2 VITE_API_URL=https://sakha-ai-prod-abc123.railway.app npm run build:prod"
```

---

## STEP 6️⃣ : Build & Deploy to GitHub Pages

### In PowerShell Terminal:

```bash
cd "c:\Users\prana\OneDrive\Desktop\Sakha 2"

# Build frontend with Railway backend URL
cd frontend
npm run build:railway

# Copy build to GitHub Pages folder
Copy-Item -Path "dist/*" -Destination "../docs" -Recurse -Force

# Commit and push to GitHub
cd ..
git add .
git commit -m "Deploy: Connect to Railway backend"
git push
```

---

## STEP 7️⃣ : Test Everything Works

### Test 1: Backend API
```
https://your-railway-url/api/docs
```
- Should see Swagger UI ✅

### Test 2: Models Endpoint
Click "Try it out" on `/api/chat/models`
- Should return list of AI models ✅

### Test 3: Complete Workflow
1. Go to: https://yubshaktijantaparty-droid.github.io/SAKHA-2/
2. Click "Start Chatting"
3. Login with:
   - Email: `test@example.com`
   - Password: `password123`
4. Click "Sign In"
5. **Verify**: Model dropdown shows multiple models ✅
6. Type message: "What is quantum computing?"
7. **Verify**: Get real AI response from OpenRouter ✅

---

## 🎉 DONE!

Your application now has:
- ✅ Real AI responses
- ✅ Multiple AI models to choose from
- ✅ Production database (MongoDB)
- ✅ Accessible on GitHub Pages
- ✅ Zero cost ($0-5/month)

---

## Troubleshooting

### Models Don't Show
- [ ] Check Railway logs for errors
- [ ] Verify API key is set correctly
- [ ] Restart Railway service

### API Calls Fail
- [ ] Check CORS_ORIGINS in Railway variables
- [ ] Verify Railway URL is correct
- [ ] Wait 30 seconds for Railway cold start

### Login Doesn't Work
- [ ] Check MongoDB connection in Railway logs
- [ ] Verify MONGODB_URI is set

### Still Having Issues?
1. Check Railway logs (Deployments → Logs)
2. Check browser console (F12)
3. Check network tab for API calls
4. Verify all variables are set

---

## Key Files Modified

- `Procfile` - Railway startup command
- `Dockerfile` - Container configuration  
- `backend/sakha/config.py` - CORS configuration
- `frontend/package.json` - Build script
- `railway.json` - Railway configuration

---

## Reference URLs

- **Railway Dashboard**: https://railway.app/dashboard
- **Your Repo**: https://github.com/yubshaktijantaparty-droid/SAKHA-2
- **GitHub Pages**: https://yubshaktijantaparty-droid.github.io/SAKHA-2/
- **OpenRouter**: https://openrouter.ai
- **MongoDB**: https://www.mongodb.com

---

**Status**: Ready to deploy! 🚀

Follow the 7 steps above and your application will work perfectly!
