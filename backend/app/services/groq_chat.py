import requests

from app.settings import settings

GROQ_CHAT_URL = "https://api.groq.com/openai/v1/chat/completions"
SYSTEM_PROMPT = (
    "You are Tyler, an effortlessly cool, confident, and sharp AI desktop assistant with the magnetic charisma, dry wit, and smooth cadence of Brad Pitt (think Tyler Durden meets cinematic charm). "
    "Speak directly, naturally, and concisely in plain text, normally in 2-3 punchy sentences. "
    "You can open allowlisted Windows desktop applications directly: Calculator, Notepad, File Explorer, Visual Studio Code, Task Manager, Terminal, Paint, Snipping Tool, Settings, Clock, and Camera. "
    "You can also open any website or URL, perform Google web searches, search videos on YouTube, and find music on Spotify."
)


class GroqChatError(RuntimeError):
    def __init__(self, message: str, status_code: int = 503) -> None:
        super().__init__(message)
        self.status_code = status_code


# ==============================================================================
# PHASE 2: THE BRAIN (Groq Chat Completion Generator)
# ==============================================================================
def generate_reply(history: list[dict[str, str]], user_text: str) -> str:
    """
    TODO (Phase 2 - Step 5):
    Send system prompt + conversation history + user text to Groq LLM completions.
    1. Verify settings.groq_api_key is set (raise GroqChatError if not).
    2. Build messages payload with SYSTEM_PROMPT, history, and new user_text.
    3. Send POST request to GROQ_CHAT_URL with temperature 0.4 and max_tokens 220.
    4. Return the trimmed assistant reply text.
    """
    if not settings.groq_api_key:
        raise GroqChatError("Groq is not configured.")

    payload = {
        "model": settings.groq_chat_model,
        "messages": [{"role": "system", "content": SYSTEM_PROMPT}, *history, {"role": "user", "content": user_text}],
        "temperature": 0.4,
        "max_tokens": 220,
    }
    try:
        response = requests.post(
            GROQ_CHAT_URL,
            headers={"Authorization": f"Bearer {settings.groq_api_key}"},
            json=payload,
            timeout=30,
        )
        response.raise_for_status()
        reply = response.json()["choices"][0]["message"]["content"]
    except (requests.RequestException, KeyError, IndexError, TypeError, ValueError) as error:
        raise GroqChatError("Groq chat request failed.") from error
    if not isinstance(reply, str) or not reply.strip():
        raise GroqChatError("Groq returned an empty reply.")
    return reply.strip()
