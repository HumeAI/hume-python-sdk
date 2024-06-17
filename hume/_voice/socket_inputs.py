"""Socket input models."""

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


class TextUserInput(BaseModel):
    """Text user input model. When provided, the text is received as a message by EVI."""

    custom_session_id: Optional[str] = None
    text: str
    type: str = "user_input"


class AssistantInput(BaseModel):
    """Assistant input model. When provided, the input is spoken by EVI."""

    custom_session_id: Optional[str] = None
    text: str
    type: str = "assistant_input"


class PauseAssistantMessage(BaseModel):
    """Pause assistant message model. When provided, responses from EVI are paused. Chat history is still saved and sent after resuming."""

    custom_session_id: Optional[str] = None
    type: str = "pause_assistant_message"


class ResumeAssistantMessage(BaseModel):
    """Resume assistant message model. When provided, responses from EVI are resumed. Chat history sent while paused will now be sent."""

    custom_session_id: Optional[str] = None
    type: str = "resume_assistant_message"
