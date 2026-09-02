# Tyler Frontend (`tyler-frontend`)

The frontend is a React 19 + Vite application. It provides the futuristic cyberpunk HUD interface, voice orb animation, microphone audio capture, SpeechSynthesis/Edge TTS playback, safe web navigation confirmation, and movable panels.

## Prerequisite

- Node.js 20 or newer
- The Tyler backend running at `http://127.0.0.1:8765`

## Quick Start

1. Set up the environment configuration:
   ```powershell
   Copy-Item .env.example .env
   ```
2. Install dependencies:
   ```powershell
   npm install
   ```
3. Start the Vite development server:
   ```powershell
   npm run dev
   ```
4. Open `http://localhost:1420` in your browser.

Tyler connects live to:
- Groq AI chat (`POST /api/chat`)
- Whisper speech-to-text (`POST /api/transcribe`)
- Edge TTS high-quality neural voice output (`POST /api/tts`)
- Safe web navigation with user confirmation
- Safe local application launching with user confirmation

## Development Scripts

```powershell
npm run dev      # Start development server
npm run lint     # Run TypeScript type checks
npm run build    # Compile production bundle to dist/
npm run preview  # Preview production build locally
```
