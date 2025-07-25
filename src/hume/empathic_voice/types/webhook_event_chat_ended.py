# This file was auto-generated by Fern from our API Definition.

import typing

import pydantic
from ...core.pydantic_utilities import IS_PYDANTIC_V2
from .webhook_event_base import WebhookEventBase
from .webhook_event_chat_status import WebhookEventChatStatus


class WebhookEventChatEnded(WebhookEventBase):
    caller_number: typing.Optional[str] = pydantic.Field(default=None)
    """
    Phone number of the caller in E.164 format (e.g., `+12223333333`). This field is included only if the Chat was created via the [Twilio phone calling](/docs/empathic-voice-interface-evi/phone-calling) integration.
    """

    custom_session_id: typing.Optional[str] = pydantic.Field(default=None)
    """
    User-defined session ID. Relevant only when employing a [custom language model](/docs/empathic-voice-interface-evi/custom-language-model) in the EVI Config.
    """

    duration_seconds: int = pydantic.Field()
    """
    Total duration of the session in seconds.
    """

    end_reason: WebhookEventChatStatus = pydantic.Field()
    """
    Reason for the session's termination.
    """

    end_time: int = pydantic.Field()
    """
    Unix timestamp (in milliseconds) indicating when the session ended.
    """

    event_name: typing.Optional[typing.Literal["chat_ended"]] = pydantic.Field(default=None)
    """
    Always `chat_ended`.
    """

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
