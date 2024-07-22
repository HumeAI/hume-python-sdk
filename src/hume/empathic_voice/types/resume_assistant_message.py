# This file was auto-generated by Fern from our API Definition.

import datetime as dt
import typing

from ...core.datetime_utils import serialize_datetime
from ...core.pydantic_utilities import deep_union_pydantic_dicts, pydantic_v1


class ResumeAssistantMessage(pydantic_v1.BaseModel):
    """
    Resume responses from EVI. Chat history sent while paused will now be sent.
    """

    type: typing.Literal["resume_assistant_message"] = pydantic_v1.Field(default="resume_assistant_message")
    """
    The type of message sent through the socket; must be `resume_assistant_message` for our server to correctly identify and process it as a Resume Assistant message.
    
    Upon resuming, if any audio input was sent during the pause, EVI will retain context from all messages sent but only respond to the last user message. (e.g., If you ask EVI two questions while paused and then send a `resume_assistant_message`, EVI will respond to the second question and have added the first question to its conversation context.)
    """

    custom_session_id: typing.Optional[str] = pydantic_v1.Field(default=None)
    """
    Used to manage conversational state, correlate frontend and backend data, and persist conversations across EVI sessions.
    """

    def json(self, **kwargs: typing.Any) -> str:
        kwargs_with_defaults: typing.Any = {"by_alias": True, "exclude_unset": True, **kwargs}
        return super().json(**kwargs_with_defaults)

    def dict(self, **kwargs: typing.Any) -> typing.Dict[str, typing.Any]:
        kwargs_with_defaults_exclude_unset: typing.Any = {"by_alias": True, "exclude_unset": True, **kwargs}
        kwargs_with_defaults_exclude_none: typing.Any = {"by_alias": True, "exclude_none": True, **kwargs}

        return deep_union_pydantic_dicts(
            super().dict(**kwargs_with_defaults_exclude_unset), super().dict(**kwargs_with_defaults_exclude_none)
        )

    class Config:
        frozen = True
        smart_union = True
        extra = pydantic_v1.Extra.allow
        json_encoders = {dt.datetime: serialize_datetime}
