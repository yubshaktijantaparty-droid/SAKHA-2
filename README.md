# SAKHA AI - ChatGPT-Like AI Assistant

**Premium AI Assistant for Chat, Image Generation, and File Analysis**

A production-ready web application combining the power of multiple AI models with a sleek, modern UI. Powered by OpenAI, Google Gemini, or DeepSeek.

## 🚀 Features

### ✨ Core Capabilities
- **AI Chat** - Seamless conversation with GPT-4, Claude, Gemini, or DeepSeek
- **Streaming Responses** - Real-time response streaming for instant feedback
- **Image Generation** - Create stunning images from text prompts (Stability AI, Hugging Face, or Replicate)
- **Chat History** - Persistent storage of all conversations
- **User Authentication** - Secure login via Supabase
- **Dark/Light Theme** - Beautiful UI with theme toggle
- **Responsive Design** - Works perfectly on desktop, tablet, and mobile

### 🎯 Perfect For
- Personal AI assistant
- Content creation
- Learning and research
- Image generation
- Code review and explanation

## 🏗️ Tech Stack

| Component | Technology |
|-----------|-----------|
| **Frontend** | React 18 + TypeScript + TailwindCSS + Vite |
| **Backend** | FastAPI + Python 3.10+ |
| **Database** | MongoDB |
| **Auth** | Supabase (PostgreSQL + Auth) |
| **State** | Zustand |
| **Deployment** | GitHub Pages (Frontend) + Render/Railway (Backend) |

## 📋 Quick Start (5 minutes)

### Prerequisites
- Node.js 18+ & npm
- Python 3.10+
- Git
- API keys (OpenAI, Gemini, or DeepSeek)

### 1. Clone & Setup

```bash
# Clone repository
git clone https://github.com/yourusername/sakha-ai.git
cd sakha-ai

# Windows
setup.bat

# Linux/Mac
bash setup.sh
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env with your API keys
```

### 3. Start Development

**Terminal 1 - Backend:**
```bash
cd backend
python run.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

### 4. Open Browser

- **App**: http://localhost:5173
- **API Docs**: http://localhost:8000/api/docs

## 📦 Deployment

### Option 1: GitHub Pages + Render (Recommended)

**Frontend → GitHub Pages (Free)**
```bash
cd frontend
npm run build
# Automatic deployment via GitHub Actions
```

**Backend → Render (Free tier)**
1. Connect repo to Render
2. Set environment variables
3. Deploy

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

### Option 2: Railway (All-in-one)

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login and deploy
railway login
railway up
```

### Option 3: Docker (Self-hosted)

```bash
docker-compose up -d
```

## 🔐 Security

⚠️ **IMPORTANT**: Never commit `.env` files with real credentials!

- API keys are stored in GitHub Secrets (for CI/CD)
- User credentials in Supabase
- Database connections via environment variables
- CORS properly configured
- Rate limiting enabled

👉 See [SECURITY_NOTICE.md](SECURITY_NOTICE.md) for critical security information.

## 📁 Project Structure

```
├── frontend/                 # React app
│   ├── src/
│   │   ├── components/      # Reusable React components
│   │   ├── pages/           # Page components
│   │   ├── services/        # API client
│   │   ├── stores/          # Zustand state management
│   │   └── types/           # TypeScript types
│   ├── package.json
│   └── vite.config.ts
│
├── backend/                  # FastAPI server
│   ├── sakha/
│   │   ├── routes/          # API endpoints
│   │   ├── services/        # Business logic
│   │   ├── database/        # MongoDB connection
│   │   ├── models/          # Data models
│   │   └── main.py          # FastAPI app
│   ├── requirements.txt
│   └── run.py
│
└── docs/                     # Documentation
```

## 🛠️ Available Commands

### Frontend
```bash
npm run dev          # Start dev server
npm run build        # Build for production
npm run preview      # Preview production build
npm run lint         # Lint code
```

### Backend
```bash
python run.py        # Start server
python -m pytest     # Run tests
```

## 🤖 Supported AI Models

### Chat
- **OpenAI**: GPT-4o, GPT-4-turbo, GPT-3.5-turbo
- **Google**: Gemini 2.5 Pro, Gemini 2.5 Flash
- **DeepSeek**: DeepSeek-Chat, DeepSeek-Reasoner
- **Anthropic**: Claude Opus, Claude Sonnet

### Image Generation
- **Stability AI**: SDXL, SD3 (Commercial, highest quality)
- **Hugging Face**: Stable Diffusion v2, SDXL (Free)
- **Replicate**: SDXL and more (Free tier available)

## 📝 API Documentation

Full API documentation available at `/api/docs` when backend is running.

### Key Endpoints
- `POST /api/chat` - Send chat message
- `POST /api/chat/stream` - Stream response
- `GET /api/chat/{chat_id}/history` - Get chat history
- `POST /api/images/generate` - Generate image
- `GET /api/images/history/{user_id}` - Image history
- `GET /api/health` - Health check

## 🧪 Testing

```bash
# Backend tests
cd backend && python -m pytest

# Frontend tests
cd frontend && npm run test
```

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## 📄 License

MIT License - see LICENSE file

## 🆘 Support

- **Issues**: GitHub Issues
- **Discussions**: GitHub Discussions
- **Email**: support@example.com

## 🙏 Acknowledgments

- [OpenAI](https://openai.com) - GPT models
- [Google](https://google.com) - Gemini models
- [Supabase](https://supabase.com) - Backend infrastructure
- [FastAPI](https://fastapi.tiangolo.com) - Backend framework
- [React](https://react.dev) - Frontend framework

---

**Made with ❤️ by [Your Name]**

🌟 If you found this project helpful, please consider giving it a star!
