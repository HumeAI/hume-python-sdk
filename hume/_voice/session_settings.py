"""Session settings model."""

from typing import Optional

from pydantic import BaseModel


class AudioSettings(BaseModel):
    """Audio settings model."""

    encoding: Optional[str] = "linear16"
    channels: Optional[int] = None
    sample_rate: Optional[int] = None


class SessionSettings(BaseModel):
    """Session settings model."""

    type: str = "session_settings"

    system_prompt: Optional[str] = None
    audio: Optional[AudioSettings] = None
