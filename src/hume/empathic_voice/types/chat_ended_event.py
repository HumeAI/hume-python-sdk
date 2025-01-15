# This file was auto-generated by Fern from our API Definition.

from .webhook_base_event import WebhookBaseEvent
from .chat_status_enum import ChatStatusEnum
import typing
from ...core.pydantic_utilities import IS_PYDANTIC_V2
import pydantic


class ChatEndedEvent(WebhookBaseEvent):
    end_time: int
    duration_seconds: int
    end_reason: ChatStatusEnum
    caller_number: typing.Optional[str] = None
    custom_session_id: typing.Optional[str] = None

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
