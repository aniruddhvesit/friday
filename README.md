# Tyler — AI Voice & Desktop Assistant

Tyler is a sleek, futuristic AI assistant inspired by Tyler Durden / Brad Pitt's voice persona, featuring a cyberpunk HUD interface, voice recognition & speech synthesis, real-time conversational intelligence, local Windows app automation, and smart web navigation.

---

## ⚡ Quick Start

### 🚀 1-Click Launch (Silent Background Mode)
- **Desktop Shortcut**: Double-click **`Tyler AI Assistant`** on your Desktop.
- **Batch / Script**: Double-click `launch-tyler.vbs` or `run-silent.bat`.
- Runs FastAPI and Vite completely silently in the background (no visible terminal windows) and opens the standalone HUD interface.

### 🛑 1-Click Stop
- **Desktop Shortcut**: Double-click **`Stop Tyler`** on your Desktop.
- **Batch / Script**: Double-click `stop-tyler.bat` or `stop-tyler.vbs`.

---

## 📂 Project Structure

```
jarvis/
├── backend/                  # FastAPI Python backend
│   ├── app/                  # Application code (API routes, services, schemas)
│   │   ├── services/         # Groq LLM, Edge TTS, local actions, web actions
│   │   └── api/              # FastAPI endpoints
│   ├── tests/                # Automated pytest suites
│   ├── run_server.py         # Windowless background server runner
│   └── requirements.txt      # Python dependencies
├── frontend/                 # React + Vite + TypeScript frontend
│   ├── src/                  # Futuristic HUD interface, components & state
│   ├── dev-server.mjs        # Programmatic Vite dev server runner
│   └── package.json          # Node dependencies and scripts
├── launch-tyler.vbs          # Native silent launcher (0 visible terminal windows)
├── stop-tyler.bat            # Clean background service terminator
├── stop-tyler.vbs            # Silent terminator with notification popup
├── run-all.bat               # Interactive / Debug launcher
└── README.md                 # Project documentation
```

---

## ✨ Features

- **Futuristic HUD UI**: Interactive Orb audio visualization, ambient audio cues, draggable telemetry panels, and standalone desktop app mode.
- **Voice Persona**: Custom Tyler Durden / Brad Pitt cinematic voice profile (`en-US-ChristopherNeural` with custom pitch/rate calibration).
- **Local Windows Automations**: Open Calculator, Notepad, VS Code, Task Manager, File Explorer, Terminal, Paint, Snipping Tool, Camera, Settings, and Clock via voice commands.
- **Web Actions**: Natural language intent parser for search, YouTube, Spotify, and direct URL navigation.
- **Silent Background Execution**: Zero flashing console windows on launch.
