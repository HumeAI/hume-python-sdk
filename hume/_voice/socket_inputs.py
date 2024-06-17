"""Socket input models."""

from typing import List, Optional

from pydantic import BaseModel


class AudioSettings(BaseModel):
    """Audio settings model."""

    encoding: Optional[str] = "linear16"
    channels: Optional[int] = None
    sample_rate: Optional[int] = None


class Tool(BaseModel):
    description: Optional[str] = None
    fallback_content: Optional[str] = None
    name: str
    parameters: str
    type: str  # "builtin" or "function"


class BuiltinToolConfig(BaseModel):
    """Built-in Tool Config model."""

    fallback_content: Optional[str] = None
    name: str = "web_search"


class SessionSettings(BaseModel):
    """Session settings model."""

    custom_session_id: Optional[str] = None
    type: str = "session_settings"
    system_prompt: Optional[str] = None
    audio: Optional[AudioSettings] = None
    language_model_api_key: Optional[str] = None
    builtin_tools: Optional[List[BuiltinToolConfig]] = None
    tools: Optional[List[Tool]]


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
