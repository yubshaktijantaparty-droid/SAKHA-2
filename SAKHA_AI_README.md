# SAKHA AI - Premium AI Assistant Platform

**Your Personal AI Assistant for Learning, Productivity, Business & Creativity**

A fully-featured ChatGPT-like web application with support for multiple AI models, image generation, file analysis, and advanced AI tools.

## 🚀 Features

### Core Features
- **AI Chat** - Seamless chat with OpenAI, DeepSeek, Google Gemini, and OpenRouter
- **Image Generation** - Generate stunning images with multiple styles and aspect ratios
- **File Analysis** - Upload and analyze PDFs, DOCX, images, and CSV files
- **Chat History** - Save and manage all your conversations locally
- **Tools Hub** - Writing, Study, Business, and Coding assistants
- **Admin Dashboard** - Monitor usage, performance, and system health

### Technical Features
- 🌐 Responsive design (Desktop, Tablet, Mobile)
- 🎨 Dark/Light theme support
- ⚡ Fast streaming responses
- 📱 PWA (Progressive Web App) support
- 🔒 Secure API with rate limiting
- 📊 Real-time performance monitoring
- 🎯 Production-ready deployment

## 🏗️ Architecture

### Frontend
- **Framework**: React 18 + TypeScript
- **Styling**: TailwindCSS
- **State Management**: Zustand
- **Build**: Vite
- **Deployment**: GitHub Pages or Vercel

### Backend
- **Framework**: FastAPI (Python)
- **Database**: MongoDB
- **AI Models**: OpenAI, DeepSeek, Google Gemini, OpenRouter
- **Deployment**: Railway or Render
- **Features**: Streaming responses, rate limiting, admin API

## 📋 Quick Start

### Prerequisites
- Node.js 18+ (for frontend)
- Python 3.10+ (for backend)
- MongoDB connection string
- API keys for AI services

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Visit: http://localhost:5173

### Backend Setup

```bash
cd backend
pip install -r requirements.txt
python run.py
```

API Docs: http://localhost:8000/api/docs

## 🔧 Environment Variables

### Backend (.env)
```env
# AI Services
OPENAI_API_KEY=sk-...
DEEPSEEK_API_KEY=sk-...
GEMINI_API_KEY=sk-...
DEFAULT_AI_PROVIDER=openai

# Database
MONGODB_URI=mongodb://...
MONGODB_DB_NAME=sakha_db

# Server
SERVER_HOST=0.0.0.0
SERVER_PORT=8000
ENVIRONMENT=development

# Security
SECRET_KEY=your-secret-key
JWT_SECRET=your-jwt-secret
```

## 🚀 Deployment

### Backend (Railway)

1. Push code to GitHub
2. Connect Railway to GitHub repo
3. Set environment variables in Railway dashboard
4. Deploy

### Frontend (GitHub Pages)

```bash
cd frontend
npm run build
```

Push to GitHub and enable GitHub Pages in repository settings.

## 📚 API Documentation

### Chat API
```bash
# Send message
POST /api/chat
{
  "message": "Hello",
  "model": "openai"
}

# Stream response
POST /api/chat/stream

# Get models
GET /api/chat/models

# Chat history
GET /api/chat/history/{chat_id}
```

### Image API
```bash
# Generate image
POST /api/images/generate
{
  "prompt": "A beautiful sunset",
  "style": "realistic"
}

# Get styles
GET /api/images/styles

# Image history
GET /api/images/history/{user_id}
```

### File API
```bash
# Upload file
POST /api/files/upload

# Analyze file
POST /api/files/{file_id}/analyze
{
  "action": "summarize"
}

# Supported types
GET /api/files/supported
```

### Admin API
```bash
# Statistics
GET /api/admin/stats

# Error logs
GET /api/admin/logs

# Performance metrics
GET /api/admin/performance
```

## 🔐 Security Features

- ✅ API key never exposed to frontend
- ✅ Environment variables for all secrets
- ✅ Rate limiting enabled
- ✅ CORS protection
- ✅ Input validation and sanitization
- ✅ XSS protection with React
- ✅ CSRF tokens for state-changing operations

## 📊 Performance

Target metrics:
- Lighthouse Score: 95+
- First Contentful Paint (FCP): < 1.5s
- Largest Contentful Paint (LCP): < 2.5s
- Response time: < 200ms
- Uptime: 99.9%

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React 18, TypeScript, TailwindCSS |
| Backend | FastAPI, Python 3.10 |
| Database | MongoDB |
| AI Models | OpenAI, DeepSeek, Gemini |
| Deployment | Railway (Backend), GitHub Pages (Frontend) |
| Monitoring | Sentry, LogRocket |

## 📁 Project Structure

```
sakha-ai/
├── frontend/
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── pages/          # Page components
│   │   ├── stores/         # Zustand stores
│   │   ├── services/       # API calls
│   │   └── App.tsx
│   ├── public/
│   ├── package.json
│   └── vite.config.ts
├── backend/
│   ├── sakha/
│   │   ├── routes/         # API endpoints
│   │   ├── services/       # Business logic
│   │   ├── ai/             # AI integrations
│   │   ├── config.py       # Configuration
│   │   └── main.py         # FastAPI app
│   ├── requirements.txt
│   └── run.py
├── docker-compose.yml
├── Dockerfile
└── README.md
```

## 🎨 UI/UX Features

- Modern glassmorphism design
- Smooth animations and transitions
- Responsive grid layouts
- Intuitive navigation
- Accessible components (WCAG 2.1)
- Light/Dark theme support
- Progressive Enhancement

## 🧪 Testing

```bash
# Frontend
cd frontend
npm run test

# Backend
cd backend
pytest tests/
```

## 📦 Building for Production

### Frontend
```bash
cd frontend
npm run build
# Output in frontend/dist/
```

### Backend
```bash
cd backend
pip install -r requirements.txt
gunicorn sakha.main:app --workers 4
```

## 🐳 Docker

```bash
docker-compose up -d
```

## 📞 Support

For issues and questions:
- GitHub Issues: [Create an issue]
- Email: support@sakha-ai.com
- Discord: [Join our community]

## 📄 License

MIT License - See LICENSE file for details

## 🙏 Acknowledgments

- Built with ❤️ by Pranab Goswami
- Powered by OpenAI, DeepSeek, and Google Gemini
- UI inspired by ChatGPT, Claude, and Perplexity

---

**SAKHA AI v1.0** | Premium AI Assistant Platform
