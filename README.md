# Friday - AI Voice & Web Assistant

Friday is an interactive AI assistant featuring a futuristic HUD interface, voice input/output, real-time conversational chat, and smart web automation planner.

---

## 📁 Project Architecture

```
friday/
├── backend/                  # FastAPI Python backend
│   ├── app/                  # Application code (API routes, services, schemas)
│   ├── tests/                # Automated pytest suites
│   ├── .env.example          # Environment variable template
│   ├── requirements.txt      # Python dependencies
│   └── run-dev.ps1           # Development startup script
├── frontend/                 # React + Vite + TypeScript frontend
│   ├── src/                  # Futuristic HUD interface, components & state
│   ├── .env.example          # Frontend configuration template
│   ├── package.json          # Node dependencies and scripts
│   └── vite.config.ts        # Vite configuration
├── .gitignore                # Root gitignore
└── README.md                 # Project documentation
```

---

## 🚀 Quick Start

### 1. Backend Setup

```bash
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
cp .env.example .env
# Edit .env and supply your GROQ_API_KEY
uvicorn app.main:app --reload --host 127.0.0.1 --port 8765
```

### 2. Frontend Setup

```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

---

## ✨ Features

- **Futuristic HUD UI**: Interactive Orb visualization, ambient audio cues, and draggable telemetry panels.
- **Voice Pipeline**: Fast Speech-to-Text (STT via Groq Whisper) & Text-to-Speech (Edge TTS).
- **Conversational Intelligence**: Memory-backed multi-turn dialogue powered by Groq LLMs.
- **Smart Web Actions**: Natural language intent parser for web queries, YouTube, Spotify, and direct navigation.
