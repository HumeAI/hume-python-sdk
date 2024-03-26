from enum import Enum
from typing import List, Optional

from pydantic import UUID4, BaseModel

from hume._common.utilities.typing_utilities import JsonObject
from hume._voice.models.configs_models import ConfigMeta


class ChatStatus(str, Enum):
    ACTIVE = "ACTIVE"
    USER_ENDED = "USER_ENDED"
    USER_TIMEOUT = "USER_TIMEOUT"
    ERROR = "ERROR"


class EventType(str, Enum):
    SYSTEM_PROMPT = "SYSTEM_PROMPT"
    USER_MESSAGE = "USER_MESSAGE"
    USER_INTERRUPTION = "USER_INTERRUPTION"
    AGENT_MESSAGE = "AGENT_MESSAGE"
    FUNCTION_CALL = "FUNCTION_CALL"


class Role(str, Enum):
    USER = "USER"
    AGENT = "AGENT"
    SYSTEM = "SYSTEM"


class FunctionCall(BaseModel):
    target: Optional[str] = None
    params: Optional[JsonObject] = None
    result: Optional[JsonObject] = None


class ChatEvent(BaseModel):
    id: UUID4
    timestamp: int
    role: Role
    type: EventType
    message_text: Optional[str] = None
    function_call: Optional[FunctionCall] = None
    emotion_features: Optional[JsonObject] = None
    metadata: Optional[JsonObject] = None


class ChatEventsResponse(BaseModel):
    id: UUID4
    resumed_from_id: Optional[UUID4] = None
    tag: Optional[str] = None
    chat_status: ChatStatus
    start_timestamp: int
    end_timestamp: Optional[int] = None
    events_page: List[ChatEvent]
    metadata: Optional[JsonObject] = None
    page_number: int
    page_size: int
    config: ConfigMeta


class ChatMessage(BaseModel):
    timestamp: int
    role: Role
    type: EventType
    message_text: Optional[str] = None
    function_call: Optional[FunctionCall] = None
    emotion_features: Optional[JsonObject] = None
    metadata: Optional[JsonObject] = None


class Chat:
    pass
