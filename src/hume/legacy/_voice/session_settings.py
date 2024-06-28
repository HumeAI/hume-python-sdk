"""Session settings model."""

from __future__ import annotations

from pydantic import BaseModel


class AudioSettings(BaseModel):
    """Audio settings model."""

    encoding: str | None = "linear16"
    channels: int | None = None
    sample_rate: int | None = None


class SessionSettings(BaseModel):
    """Session settings model."""

    type: str = "session_settings"

    system_prompt: str | None = None
    audio: AudioSettings | None = None
