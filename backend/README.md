# Tyler backend

The backend is a FastAPI service that keeps credentials server-side and exposes chat, speech, action-planning, and local desktop task endpoints.

## Prerequisites

- Python 3.11+
- A Groq API key

## Install and run

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Edit `.env` and set `GROQ_API_KEY`. Then run:

```powershell
.\run-dev.ps1
```

The API binds to `127.0.0.1:8765` by default. Check it at `http://127.0.0.1:8765/api/health`.

## Environment variables

| Variable | Purpose |
| --- | --- |
| `GROQ_API_KEY` | Required secret used for Groq chat and transcription. |
| `GROQ_CHAT_MODEL` | Optional Groq chat model override. |
| `TYLER_BACKEND_HOST` / `TYLER_BACKEND_PORT` | Local bind address and port. Keep the host loopback for local use. |
| `TYLER_ALLOWED_ORIGINS` | Comma-separated exact frontend origins for CORS. Never use `*`. |
| `TYLER_LOCAL_ACTIONS_ENABLED` | Defaults to `true`. Enables the Windows application allowlist. |

Never commit `.env`.

## API contracts

| Method and path | Request | Response | Purpose |
| --- | --- | --- | --- |
| `GET /api/health` | — | `{ "status": "ok" }` | Service health. |
| `POST /api/chat` | `{ "sessionId": "UUID", "text": "..." }` | `{ "sessionId": "UUID", "reply": "...", "turnsRetained": 0-6 }` | Groq chat with in-memory context. |
| `GET /api/voices` | — | `{ "voices": [{ "id", "label" }] }` | Edge TTS voice choices. |
| `POST /api/tts` | `{ "text": "...", "voiceId": "..." }` | `audio/mpeg` | Synthesized voice audio. |
| `POST /api/transcribe` | multipart field `audio` | `{ "transcript": "..." }` | Groq Whisper transcription. Audio is capped at 10 MB. |
| `POST /api/web-actions/plan` | `{ "text": "..." }` | `{ "kind", "label", "url" }` | Produces a constrained website/search destination for frontend confirmation. |
| `GET /api/local-actions/status` | — | `{ "enabled": boolean }` | Local bridge availability. |
| `POST /api/local-actions/plan` | `{ "text": "..." }` | `{ "kind", "appId", "label", "requiresConfirmation" }` | Plans one allowlisted app. |
| `POST /api/local-actions/execute` | `{ "appId": "...", "confirmed": true }` | `{ "ok": true, "message": "..." }` | Opens a fixed allowlisted Windows app. |

## Safety boundary

The planner produces browser websites/searches and safe allowlisted Windows applications with user confirmation. It rejects non-local browser origins and does not accept arbitrary shell commands.

## Tests

```powershell
cd backend
python -m pytest tests -q
```
