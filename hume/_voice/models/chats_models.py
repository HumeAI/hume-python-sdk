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
    emotion_features: Optional[str] = None
    metadata: Optional[str] = None


class ChatEventsResponse(BaseModel):
    """Response model for a page of EVI chat events."""

    id: UUID4
    tag: Optional[str] = None
    status: ChatStatus
    start_timestamp: int
    end_timestamp: Optional[int] = None
    events_page: List[ChatEvent]
    metadata: Optional[str] = None
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
    emotion_features: Optional[str] = None
    metadata: Optional[str] = None


class ChatResponse(BaseModel):
    """Response model for an EVI chat."""

    id: str
    chat_group_id: str
    tag: Optional[str] = None
    status: Optional[ChatStatus]
    start_timestamp: int
    end_timestamp: int
    metadata: Optional[str] = None
    config: Optional[ConfigMeta] = None


class ChatsResponse(BaseModel):
    """Response model for a page of EVI chats."""

    chats_page: List[ChatResponse]
    page_number: int
    page_size: int


class VoiceChat(BaseModel):
    """Voice chat model."""

    id: str
    chat_group_id: str
    start_timestamp: int
    end_timestamp: int


class ChatGroupResponse(BaseModel):
    """Response model for an EVI chat group."""

    id: str
    first_start_timestamp: int
    most_recent_start_timestamp: int
    num_chats: int
    is_active: bool


class ChatGroupsResponse(BaseModel):
    """Response model for a page of EVI chat groups."""

    chat_groups_page: List[ChatGroupResponse]
    page_number: int
    page_size: int


class VoiceChatGroup(BaseModel):
    """Voice chat group model."""

    id: str
    first_start_timestamp: int
    most_recent_start_timestamp: int
    num_chats: int
    is_active: bool


class ChatGroupEvent(BaseModel):
    """Chat group event model."""

    id: UUID4
    chat_id: UUID4
    timestamp: int
    role: Role
    type: EventType
    message_text: Optional[str] = None
    emotion_features: Optional[str] = None
    metadata: Optional[str] = None


class ChatGroupEventsResponse(BaseModel):
    """Response model for a page of EVI chat group events."""

    id: UUID4
    events_page: List[ChatGroupEvent]
    page_number: int
    page_size: int
    pagination_direction: str
