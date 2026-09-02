import json
import re
from typing import Literal
from urllib.parse import quote_plus, urlparse, urlunparse

import requests

from app.settings import settings

PlanKind = Literal["web_search", "youtube_search", "spotify_search"]

PLANNER_PROMPT = """Classify a browser-navigation request. Return JSON only:
{"kind":"web_search|youtube_search|spotify_search","query":"short search text"}.
Use youtube_search for requests to find a YouTube video, song, audio, or channel.
Use spotify_search for requests to find music, an artist, album, podcast, or playlist on Spotify.
Use web_search for every other website/search request. Never return a URL, command,
file path, app name, or explanation."""


def _model_classification(text: str) -> dict[str, str] | None:
    if not settings.groq_api_key:
        return None
    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {settings.groq_api_key}"},
            json={
                "model": settings.groq_chat_model,
                "messages": [{"role": "system", "content": PLANNER_PROMPT}, {"role": "user", "content": text}],
                "temperature": 0,
                "max_tokens": 80,
            },
            timeout=10,
        )
        response.raise_for_status()
        result = json.loads(response.json()["choices"][0]["message"]["content"])
        if result.get("kind") in {"web_search", "youtube_search", "spotify_search"} and isinstance(result.get("query"), str):
            return {"kind": result["kind"], "query": result["query"].strip()}
    except (requests.RequestException, KeyError, IndexError, TypeError, ValueError, json.JSONDecodeError):
        return None
    return None


# ==============================================================================
# PHASE 4: THE HANDS (Safe Web Action Destination Planner)
# ==============================================================================
def make_web_action_plan(text: str) -> dict[str, str]:
    """
    TODO (Phase 4 - Step 9):
    Classify user navigation request and return safe destination plan {kind, label, url}.
    - Explicit URL -> open_website
    - YouTube search -> youtube_search
    - Spotify search -> spotify_search
    - Other search -> web_search
    """
    url_match = re.search(r"https?://[^\s<>\"]+", text)
    if url_match:
        raw_url = url_match.group(0).rstrip(".,!?;:)")
        parsed = urlparse(raw_url)
        if parsed.netloc:
            return {"kind": "open_website", "label": parsed.netloc, "url": urlunparse(parsed)}

    classification = _model_classification(text)
    if classification is None:
        normalized = " ".join(text.lower().split())
        if "youtube" in normalized:
            kind = "youtube_search"
        elif "spotify" in normalized:
            kind = "spotify_search"
        else:
            kind = "web_search"
        query = re.sub(r"\b(please|open|search|find|look for|play|on youtube|on spotify|on the web|online)\b", " ", text, flags=re.IGNORECASE)
        query = " ".join(query.split()).strip()
    else:
        kind = classification["kind"]
        query = classification["query"]

    if not query:
        query = text.strip()
    if kind == "youtube_search":
        return {"kind": kind, "label": f"YouTube search: {query}", "url": f"https://www.youtube.com/results?search_query={quote_plus(query)}"}
    if kind == "spotify_search":
        return {"kind": kind, "label": f"Spotify search: {query}", "url": f"https://open.spotify.com/search/{quote_plus(query)}"}
    return {"kind": "web_search", "label": f"Web search: {query}", "url": f"https://www.google.com/search?q={quote_plus(query)}"}

