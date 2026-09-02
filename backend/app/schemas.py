from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class BaseSchema(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class ChatRequest(BaseSchema):
    session_id: UUID
    text: str = Field(min_length=1, max_length=2_000)


class ChatResponse(BaseSchema):
    session_id: UUID
    reply: str
    turns_retained: int = Field(ge=0, le=6)


class Voice(BaseSchema):
    id: str
    label: str


class VoicesResponse(BaseSchema):
    voices: list[Voice]


class TtsRequest(BaseSchema):
    text: str = Field(min_length=1, max_length=2_000)
    voice_id: str


class TranscriptResponse(BaseSchema):
    transcript: str


class WebActionPlanRequest(BaseSchema):
    text: str = Field(min_length=1, max_length=2_000)


class WebActionPlanResponse(BaseSchema):
    kind: Literal["open_website", "web_search", "youtube_search", "spotify_search"]
    label: str = Field(min_length=1, max_length=160)
    url: str = Field(min_length=1, max_length=2_000)


LocalAppIdType = Literal[
    "calculator",
    "notepad",
    "file_explorer",
    "vscode",
    "task_manager",
    "terminal",
    "paint",
    "snipping_tool",
    "settings",
    "clock",
    "camera",
]


class LocalActionPlanRequest(BaseSchema):
    text: str = Field(min_length=1, max_length=2_000)


class LocalActionPlanResponse(BaseSchema):
    kind: Literal["open_local_app"]
    app_id: LocalAppIdType
    label: str = Field(min_length=1, max_length=160)
    requires_confirmation: bool


class LocalActionExecuteRequest(BaseSchema):
    app_id: LocalAppIdType
    confirmed: Literal[True]


class LocalActionExecuteResponse(BaseSchema):
    ok: bool
    message: str


class LocalActionStatusResponse(BaseSchema):
    enabled: bool
