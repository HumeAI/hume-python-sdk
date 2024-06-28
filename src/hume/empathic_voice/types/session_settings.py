# This file was auto-generated by Fern from our API Definition.

import datetime as dt
import typing

from ...core.datetime_utils import serialize_datetime
from ...core.pydantic_utilities import deep_union_pydantic_dicts, pydantic_v1
from .audio_configuration import AudioConfiguration
from .builtin_tool_config import BuiltinToolConfig
from .tool import Tool


class SessionSettings(pydantic_v1.BaseModel):
    """
    Settings for this chat session.
    """

    audio: typing.Optional[AudioConfiguration] = pydantic_v1.Field(default=None)
    """
    Audio configuration.
    """

    builtin_tools: typing.Optional[typing.List[BuiltinToolConfig]] = pydantic_v1.Field(default=None)
    """
    List of builtin tools to enable.
    """

    custom_session_id: typing.Optional[str] = pydantic_v1.Field(default=None)
    """
    Used to manage conversational state, correlate frontend and backend data, and persist conversations across EVI sessions.
    """

    language_model_api_key: typing.Optional[str] = pydantic_v1.Field(default=None)
    """
    Third party API key for the language model used for non-Hume models.
    """

    system_prompt: typing.Optional[str] = pydantic_v1.Field(default=None)
    """
    Instructions for how the system should respond to the user. Set to null to use the default system prompt.
    """

    tools: typing.Optional[typing.List[Tool]] = pydantic_v1.Field(default=None)
    """
    List of tools to enable.
    """

    type: typing.Literal["session_settings"] = pydantic_v1.Field(default="session_settings")
    """
    The type of message sent through the socket; for a Session Settings message, this must be 'session_settings'.
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