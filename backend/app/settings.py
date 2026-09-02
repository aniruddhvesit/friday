from dataclasses import dataclass
import os

from dotenv import load_dotenv

load_dotenv()


def parse_origins(value: str) -> tuple[str, ...]:
    return tuple(origin.strip().rstrip("/") for origin in value.split(",") if origin.strip())


def parse_bool(value: str) -> bool:
    return value.strip().lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class Settings:
    backend_host: str = os.getenv("TYLER_BACKEND_HOST", os.getenv("JARVIS_BACKEND_HOST", "127.0.0.1"))
    backend_port: int = int(os.getenv("TYLER_BACKEND_PORT", os.getenv("JARVIS_BACKEND_PORT", "8765")))
    groq_api_key: str = os.getenv("GROQ_API_KEY", "")
    groq_chat_model: str = os.getenv("GROQ_CHAT_MODEL", "openai/gpt-oss-20b")
    allowed_origins: tuple[str, ...] = parse_origins(
        os.getenv("TYLER_ALLOWED_ORIGINS", os.getenv("JARVIS_ALLOWED_ORIGINS", "http://localhost:1420,http://127.0.0.1:1420"))
    )
    local_actions_enabled: bool = parse_bool(
        os.getenv("TYLER_LOCAL_ACTIONS_ENABLED", os.getenv("JARVIS_LOCAL_ACTIONS_ENABLED", "true"))
    )


settings = Settings()
