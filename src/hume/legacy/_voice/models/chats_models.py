"""API request and response models for EVI chats."""

from __future__ import annotations

from enum import Enum

from pydantic import UUID4, BaseModel

from hume.legacy._common.utilities.typing_utilities import JsonObject
from hume.legacy._voice.models.configs_models import ConfigMeta


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

    target: str | None = None
    params: JsonObject | None = None
    result: JsonObject | None = None


class ChatEvent(BaseModel):
    """Chat event model."""

    id: UUID4
    timestamp: int
    role: Role
    type: EventType
    message_text: str | None = None
    function_call: FunctionCall | None = None
    emotion_features: str | None = None
    metadata: str | None = None


class ChatEventsResponse(BaseModel):
    """Response model for a page of EVI chat events."""

    id: UUID4
    tag: str | None = None
    status: ChatStatus
    start_timestamp: int
    end_timestamp: int | None = None
    events_page: list[ChatEvent]
    metadata: str | None = None
    page_number: int
    page_size: int
    config: ConfigMeta


class ChatMessage(BaseModel):
    """Chat message model."""

    timestamp: int
    role: Role
    type: EventType
    message_text: str | None = None
    function_call: FunctionCall | None = None
    emotion_features: str | None = None
    metadata: str | None = None


class ChatResponse(BaseModel):
    """Response model for an EVI chat."""

    id: str
    chat_group_id: str
    tag: str | None = None
    status: ChatStatus | None
    start_timestamp: int
    end_timestamp: int
    metadata: str | None = None
    config: ConfigMeta | None = None


class ChatsResponse(BaseModel):
    """Response model for a page of EVI chats."""

    chats_page: list[ChatResponse]
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

    chat_groups_page: list[ChatGroupResponse]
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
    message_text: str | None = None
    emotion_features: str | None = None
    metadata: str | None = None


class ChatGroupEventsResponse(BaseModel):
    """Response model for a page of EVI chat group events."""

    id: UUID4
    events_page: list[ChatGroupEvent]
    page_number: int
    page_size: int
    pagination_direction: str
