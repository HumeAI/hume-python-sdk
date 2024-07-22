# This file was auto-generated by Fern from our API Definition.

import datetime as dt
import typing

from ...core.datetime_utils import serialize_datetime
from ...core.pydantic_utilities import deep_union_pydantic_dicts, pydantic_v1
from .error_level import ErrorLevel
from .tool_type import ToolType


class ToolErrorMessage(pydantic_v1.BaseModel):
    """
    When provided, the output is a function call error.
    """

    type: typing.Literal["tool_error"] = pydantic_v1.Field(default="tool_error")
    """
    The type of message sent through the socket; for a Tool Error message, this must be `tool_error`.
    
    Upon receiving a [Tool Call message](/reference/empathic-voice-interface-evi/chat/chat#receive.Tool%20Call%20Message.type) and failing to invoke the function, this message is sent to notify EVI of the tool's failure.
    """

    custom_session_id: typing.Optional[str] = pydantic_v1.Field(default=None)
    """
    Used to manage conversational state, correlate frontend and backend data, and persist conversations across EVI sessions.
    """

    tool_type: typing.Optional[ToolType] = pydantic_v1.Field(default=None)
    """
    Type of tool called. Either `builtin` for natively implemented tools, like web search, or `function` for user-defined tools.
    """

    tool_call_id: str = pydantic_v1.Field()
    """
    The unique identifier for a specific tool call instance.
    
    This ID is used to track the request and response of a particular tool invocation, ensuring that the Tool Error message is linked to the appropriate tool call request. The specified `tool_call_id` must match the one received in the [Tool Call message](/reference/empathic-voice-interface-evi/chat/chat#receive.Tool%20Call%20Message.type).
    """

    content: typing.Optional[str] = pydantic_v1.Field(default=None)
    """
    Optional text passed to the supplemental LLM in place of the tool call result. The LLM then uses this text to generate a response back to the user, ensuring continuity in the conversation if the tool errors.
    """

    error: str = pydantic_v1.Field()
    """
    Error message from the tool call, not exposed to the LLM or user.
    """

    code: typing.Optional[str] = pydantic_v1.Field(default=None)
    """
    Error code. Identifies the type of error encountered.
    """

    level: typing.Optional[ErrorLevel] = pydantic_v1.Field(default=None)
    """
    Indicates the severity of an error; for a Tool Error message, this must be `warn` to signal an unexpected event.
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
