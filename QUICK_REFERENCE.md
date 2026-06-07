# 🎯 SAKHA AI - Quick Reference Card

## 🚀 QUICK START (2 minutes)

### 1. Setup
```bash
# Windows
setup.bat

# Linux/Mac
bash setup.sh
```

### 2. Run
**Terminal 1:**
```bash
cd backend && python run.py
```

**Terminal 2:**
```bash
cd frontend && npm run dev
```

### 3. Access
- Frontend: http://localhost:5173
- API Docs: http://localhost:8000/api/docs
- Health: http://localhost:8000/api/health

---

## 📁 PROJECT FILES

### Backend (Python/FastAPI)
```
backend/
├── run.py                    # Start server
├── requirements.txt          # Dependencies
└── sakha/
    ├── main.py              # FastAPI app
    ├── config.py            # Settings
    ├── routes/              # API endpoints
    │   ├── chat.py
    │   ├── images.py
    │   ├── files.py
    │   └── admin.py
    ├── services/            # Business logic
    │   ├── ai_service.py
    │   ├── image_service.py
    │   └── file_service.py
    └── utils/
        └── logging_config.py
```

### Frontend (React/TypeScript)
```
frontend/
├── package.json
├── vite.config.ts
├── tailwind.config.js
├── index.html
└── src/
    ├── App.tsx
    ├── main.tsx
    ├── index.css
    ├── components/          # UI Components
    │   ├── Layout.tsx
    │   ├── Sidebar.tsx
    │   ├── ChatView.tsx
    │   ├── ChatInput.tsx
    │   ├── Message.tsx
    │   └── ThemeToggle.tsx
    ├── pages/               # Pages
    │   ├── ImageGenerator.tsx
    │   ├── FileAnalysis.tsx
    │   ├── ToolsHub.tsx
    │   ├── AdminDashboard.tsx
    │   └── LandingPage.tsx
    ├── services/            # API
    │   └── api.ts
    └── stores/              # State
        ├── chat.ts
        └── app.ts
```

---

## 🔧 CONFIGURATION

### .env Variables (Required)
```env
# AI Services
OPENAI_API_KEY=sk-...
DEEPSEEK_API_KEY=sk-...
GEMINI_API_KEY=...

# Database
MONGODB_URI=mongodb://...
MONGODB_DB_NAME=sakha_db

# Server
SERVER_PORT=8000
ENVIRONMENT=development
```

### Get API Keys
- **OpenAI**: https://platform.openai.com
- **DeepSeek**: https://platform.deepseek.com
- **Gemini**: https://makersuite.google.com
- **MongoDB**: https://www.mongodb.com

---

## 🔌 API ENDPOINTS

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/api/chat` | Send message |
| POST | `/api/chat/stream` | Stream response |
| GET | `/api/chat/models` | Get AI models |
| POST | `/api/images/generate` | Generate image |
| GET | `/api/images/styles` | Get image styles |
| POST | `/api/files/upload` | Upload file |
| POST | `/api/files/{id}/analyze` | Analyze file |
| GET | `/api/admin/stats` | Admin stats |
| GET | `/api/health` | Health check |

---

## 🛠️ COMMON COMMANDS

### Backend
```bash
cd backend
python -m venv venv          # Create venv
source venv/bin/activate     # Activate (Linux/Mac)
venv\Scripts\activate        # Activate (Windows)
pip install -r requirements.txt  # Install deps
python run.py                # Start server
```

### Frontend
```bash
cd frontend
npm install                  # Install deps
npm run dev                  # Start dev server
npm run build                # Build for prod
npm run preview              # Preview build
```

### Docker
```bash
docker-compose up            # Start all services
docker-compose down          # Stop all services
docker-compose logs -f       # View logs
```

---

## 📚 DOCUMENTATION FILES

| File | Contains |
|------|----------|
| PROJECT_COMPLETE.md | Project overview & features |
| SETUP_GUIDE.md | Detailed setup instructions |
| DEPLOYMENT_GUIDE.md | Production deployment |
| ARCHITECTURE.md | System design & architecture |
| SAKHA_AI_README.md | Complete documentation |
| .env.example | Environment template |

---

## 🚀 DEPLOYMENT

### Railway (Recommended)
1. Push to GitHub
2. Connect Railway to repo
3. Set environment variables
4. Auto-deploy on push

### Docker
```bash
docker-compose up -d
# App at: http://localhost:5173
# API at: http://localhost:8000
```

### Vercel + Render
- Frontend → Vercel
- Backend → Render

---

## ✨ KEY FEATURES

### Chat
- Multi-model support (OpenAI, DeepSeek, Gemini)
- Streaming responses
- Chat history
- Markdown rendering
- Code syntax highlighting

### Images
- Text-to-image generation
- Multiple styles (realistic, anime, etc.)
- Aspect ratios
- History tracking

### Files
- PDF, DOCX, TXT, Images, CSV
- Summarization
- Analysis
- Data extraction

### Admin
- Usage statistics
- Performance metrics
- Error logs
- System monitoring

---

## 🎨 UI COMPONENTS

### Pages Implemented
1. **Chat Page** - Main interface
2. **Image Generator** - Text-to-image
3. **File Analysis** - Document processing
4. **Tools Hub** - Tool directory
5. **Admin Dashboard** - Monitoring
6. **Landing Page** - Marketing page

### Features
- Dark/Light theme
- Responsive design
- Markdown support
- Real-time streaming
- PWA support

---

## 📊 TECH STACK

| Layer | Technology |
|-------|-----------|
| Frontend | React 18, TypeScript, TailwindCSS |
| Backend | FastAPI, Python 3.10 |
| State | Zustand |
| Build | Vite, npm |
| Database | MongoDB |
| AI Models | OpenAI, DeepSeek, Gemini |
| Deployment | Railway, Docker |

---

## 🆘 TROUBLESHOOTING

### Backend won't start
```bash
# Check Python version
python --version  # Should be 3.10+

# Verify dependencies
pip list

# Check .env file
cat .env
```

### Frontend build fails
```bash
# Clear cache
rm -rf node_modules package-lock.json
npm install
```

### MongoDB connection error
```bash
# Verify URI format
# Test locally: mongodb://localhost:27017
# Atlas: mongodb+srv://user:pass@cluster...
```

### Port already in use
```bash
# Change port in .env
SERVER_PORT=8001

# Or kill process
lsof -i :8000  # Find process
kill -9 <PID>  # Kill process
```

---

## 📞 SUPPORT

- **Backend**: FastAPI docs at `/api/docs`
- **Docs**: Read documentation files
- **Issues**: Check GitHub issues
- **Email**: Check project README

---

## ✅ CHECKLIST

Before deploying to production:
- [ ] Environment variables set correctly
- [ ] API keys added and working
- [ ] MongoDB connected
- [ ] Tests passed
- [ ] Build successful
- [ ] No console errors
- [ ] Rate limiting enabled
- [ ] CORS configured
- [ ] Error handling tested

---

## 🎉 YOU'RE READY!

Your SAKHA AI platform is fully functional and ready for:
- ✅ Development
- ✅ Testing
- ✅ Deployment
- ✅ Production use

**Next Step**: Read PROJECT_COMPLETE.md for detailed overview

---

**SAKHA AI v1.0** | Premium AI Assistant Platform
Created for: Pranab Goswami | Date: 2024
