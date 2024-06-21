"""Socket input models."""

# NOTE:
# - reference API definition for updated query parameter descriptions:
#   https://dev.hume.ai/reference/empathic-voice-interface-evi/chat/chat

from typing import List, Optional

from pydantic import BaseModel


class AudioSettings(BaseModel):
    """Audio settings model."""

    encoding: str = "linear16"  # linear16 is required
    channels: Optional[int] = None
    sample_rate: Optional[int] = None


class Tool(BaseModel):
    """Tool model."""

    description: Optional[str] = None
    fallback_content: Optional[str] = None
    name: str
    parameters: str
    type: str  # "builtin" or "function"


class Context(BaseModel):
    """Context model."""

    text: str
    type: Optional[str]  # editable, persistent, temporary


class BuiltinToolConfig(BaseModel):
    """Built-in Tool Config model."""

    fallback_content: Optional[str] = None
    name: str = "web_search"


class SessionSettings(BaseModel):
    """Session settings model."""

    context: Optional[Context] = None
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
    """
    Pause assistant message model.

    When provided, responses from EVI are paused.
    Chat history is still saved and sent after resuming.
    """

    custom_session_id: Optional[str] = None
    type: str = "pause_assistant_message"


class ResumeAssistantMessage(BaseModel):
    """
    Resume assistant message model.

    When provided, responses from EVI are resumed.
    Chat history sent while paused will now be sent.
    """

    custom_session_id: Optional[str] = None
    type: str = "resume_assistant_message"


class ToolErrorMessage(BaseModel):
    """Tool error message model. When provided, the output is a function call error."""

    code: Optional[str] = None
    content: Optional[str] = None
    custom_session_id: Optional[str] = None
    error: str
    level: Optional[str] = "warn"
    tool_call_id: str
    tool_type: str  # "builtin" or "function"
    type: str = "tool_error"


class ToolResponseMessage(BaseModel):
    """Tool response message model. When provided, the output is a function call response."""

    content: str
    custom_session_id: Optional[str] = None
    tool_call_id: str
    tool_name: Optional[str]
    tool_type: str  # "builtin" or "function"
    type: str = "tool_response"
