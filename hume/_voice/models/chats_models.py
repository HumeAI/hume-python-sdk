"""API request and response models for EVI chats."""

from enum import Enum
from typing import List, Optional

from pydantic import UUID4, BaseModel

from hume._common.utilities.typing_utilities import JsonObject
from hume._voice.models.configs_models import ConfigMeta


class ChatStatus(str, Enum):
    """Status codes for EVI chats."""

    ACTIVE = "ACTIVE"
    USER_ENDED = "USER_ENDED"
    USER_TIMEOUT = "USER_TIMEOUT"
    ERROR = "ERROR"


class EventType(str, Enum):
    """Identifier for the type of event in an EVI session."""

    SYSTEM_PROMPT = "SYSTEM_PROMPT"
    USER_MESSAGE = "USER_MESSAGE"
    USER_INTERRUPTION = "USER_INTERRUPTION"
    AGENT_MESSAGE = "AGENT_MESSAGE"
    FUNCTION_CALL = "FUNCTION_CALL"


class Role(str, Enum):
    """Identifier for the speaker of a turn in an EVI session."""

    USER = "USER"
    AGENT = "AGENT"
    SYSTEM = "SYSTEM"


class FunctionCall(BaseModel):
    """Function call model."""

    target: Optional[str] = None
    params: Optional[JsonObject] = None
    result: Optional[JsonObject] = None


class ChatEvent(BaseModel):
    """Chat event model."""

    id: UUID4
    timestamp: int
    role: Role
    type: EventType
    message_text: Optional[str] = None
    function_call: Optional[FunctionCall] = None
    emotion_features: Optional[JsonObject] = None
    metadata: Optional[JsonObject] = None


class ChatEventsResponse(BaseModel):
    """Response model for a page of EVI chat events."""

    id: UUID4
    resumed_from_id: Optional[UUID4] = None
    tag: Optional[str] = None
    status: ChatStatus
    start_timestamp: int
    end_timestamp: Optional[int] = None
    events_page: List[ChatEvent]
    metadata: Optional[JsonObject] = None
    page_number: int
    page_size: int
    config: ConfigMeta


class ChatMessage(BaseModel):
    """Chat message model."""

    timestamp: int
    role: Role
    type: EventType
    message_text: Optional[str] = None
    function_call: Optional[FunctionCall] = None
    emotion_features: Optional[JsonObject] = None
    metadata: Optional[JsonObject] = None


class ChatResponse(BaseModel):
    """Response model for an EVI chat."""

    id: str
    resumed_from_id: Optional[UUID4] = None
    tag: Optional[str] = None
    status: Optional[ChatStatus]
    start_timestamp: int
    end_timestamp: int
    metadata: Optional[JsonObject] = None
    config: ConfigMeta


class ChatsResponse(BaseModel):
    """Response model for a page of EVI chats."""

    chats_page: List[ChatResponse]
    page_number: int
    page_size: int


class VoiceChat(BaseModel):
    """Voice chat model."""

    id: str
