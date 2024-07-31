# This file was auto-generated by Fern from our API Definition.

import datetime as dt
import typing

from ...core.datetime_utils import serialize_datetime
from ...core.pydantic_utilities import deep_union_pydantic_dicts, pydantic_v1


class AudioInput(pydantic_v1.BaseModel):
    """
    When provided, the input is audio.
    """

    type: typing.Literal["audio_input"] = pydantic_v1.Field(default="audio_input")
    """
    The type of message sent through the socket; must be `audio_input` for our server to correctly identify and process it as an Audio Input message.
    
    This message is used for sending audio input data to EVI for processing and expression measurement. Audio data should be sent as a continuous stream, encoded in Base64.
    """

    custom_session_id: typing.Optional[str] = pydantic_v1.Field(default=None)
    """
    Used to manage conversational state, correlate frontend and backend data, and persist conversations across EVI sessions.
    """

    data: str = pydantic_v1.Field()
    """
    Base64 encoded audio input to insert into the conversation.
    
    The content of an Audio Input message is treated as the user’s speech to EVI and must be streamed continuously. Pre-recorded audio files are not supported.
    
    For optimal transcription quality, the audio data should be transmitted in small chunks.
    
    Hume recommends streaming audio with a buffer window of 20 milliseconds (ms), or 100 milliseconds (ms) for web applications.
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
