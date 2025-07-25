# This file was auto-generated by Fern from our API Definition.

import typing

import pydantic
from ...core.pydantic_utilities import IS_PYDANTIC_V2, UniversalBaseModel
from .return_chat_status import ReturnChatStatus
from .return_config_spec import ReturnConfigSpec


class ReturnChat(UniversalBaseModel):
    """
    A description of chat and its status
    """

    id: str = pydantic.Field()
    """
    Identifier for a Chat. Formatted as a UUID.
    """

    chat_group_id: str = pydantic.Field()
    """
    Identifier for the Chat Group. Any chat resumed from this Chat will have the same `chat_group_id`. Formatted as a UUID.
    """

    status: ReturnChatStatus = pydantic.Field()
    """
    Indicates the current state of the chat. There are six possible statuses:
    
    - `ACTIVE`: The chat is currently active and ongoing.
    
    - `USER_ENDED`: The chat was manually ended by the user.
    
    - `USER_TIMEOUT`: The chat ended due to a user-defined timeout.
    
    - `MAX_DURATION_TIMEOUT`: The chat ended because it reached the maximum allowed duration.
    
    - `INACTIVITY_TIMEOUT`: The chat ended due to an inactivity timeout.
    
    - `ERROR`: The chat ended unexpectedly due to an error.
    """

    start_timestamp: int = pydantic.Field()
    """
    Time at which the Chat started. Measured in seconds since the Unix epoch.
    """

    end_timestamp: typing.Optional[int] = pydantic.Field(default=None)
    """
    Time at which the Chat ended. Measured in seconds since the Unix epoch.
    """

    event_count: typing.Optional[int] = pydantic.Field(default=None)
    """
    The total number of events currently in this chat.
    """

    metadata: typing.Optional[str] = pydantic.Field(default=None)
    """
    Stringified JSON with additional metadata about the chat.
    """

    config: typing.Optional[ReturnConfigSpec] = None

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
