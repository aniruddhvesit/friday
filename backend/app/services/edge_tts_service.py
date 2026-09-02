from dataclasses import dataclass
import edge_tts

from app.schemas import Voice


@dataclass(frozen=True)
class VoiceProfile:
    id: str
    label: str
    edge_voice: str
    pitch: str = "+0Hz"
    rate: str = "+0%"


VOICE_PROFILES: tuple[VoiceProfile, ...] = (
    VoiceProfile(
        id="tyler-brad-pitt",
        label="Tyler — Brad Pitt (Cinematic)",
        edge_voice="en-US-ChristopherNeural",
        pitch="-4Hz",
        rate="+1%",
    ),
    VoiceProfile(
        id="tyler-durden-gritty",
        label="Tyler — Gritty & Confident",
        edge_voice="en-US-EricNeural",
        pitch="-3Hz",
        rate="+0%",
    ),
    VoiceProfile(
        id="tyler-smooth",
        label="Tyler — Smooth & Charismatic",
        edge_voice="en-US-AndrewMultilingualNeural",
        pitch="-2Hz",
        rate="+0%",
    ),
    VoiceProfile(
        id="en-US-GuyNeural",
        label="Guy — US English",
        edge_voice="en-US-GuyNeural",
        pitch="+0Hz",
        rate="+0%",
    ),
    VoiceProfile(
        id="en-GB-RyanNeural",
        label="Ryan — UK English",
        edge_voice="en-GB-RyanNeural",
        pitch="+0Hz",
        rate="+0%",
    ),
    VoiceProfile(
        id="en-US-JennyNeural",
        label="Jenny — US English",
        edge_voice="en-US-JennyNeural",
        pitch="+0Hz",
        rate="+0%",
    ),
)

VOICE_MAP: dict[str, VoiceProfile] = {vp.id: vp for vp in VOICE_PROFILES}
VOICE_IDS: set[str] = set(VOICE_MAP.keys())


class EdgeTtsError(RuntimeError):
    pass


def available_voices() -> list[Voice]:
    return [Voice(id=vp.id, label=vp.label) for vp in VOICE_PROFILES]


# ==============================================================================
# PHASE 3: THE MOUTH (Neural Text-to-Speech Streaming)
# ==============================================================================
async def generate_speech(text: str, voice_id: str) -> bytes:
    """
    Synthesize text into MP3 audio bytes using Microsoft Edge TTS with profile-tuned pitch and rate.
    """
    if voice_id not in VOICE_IDS:
        raise EdgeTtsError("That voice is not available.")

    profile = VOICE_MAP[voice_id]
    audio = bytearray()
    try:
        stream = edge_tts.Communicate(
            text=text,
            voice=profile.edge_voice,
            pitch=profile.pitch,
            rate=profile.rate,
        )
        async for chunk in stream.stream():
            if chunk.get("type") == "audio":
                audio.extend(chunk.get("data", b""))
    except Exception as error:
        raise EdgeTtsError("Text-to-speech generation failed.") from error
    return bytes(audio)

