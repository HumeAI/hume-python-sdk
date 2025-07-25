# This file was auto-generated by Fern from our API Definition.

import typing

import pydantic
from ...core.pydantic_utilities import IS_PYDANTIC_V2, UniversalBaseModel


class AudioInput(UniversalBaseModel):
    """
    When provided, the input is audio.
    """

    custom_session_id: typing.Optional[str] = pydantic.Field(default=None)
    """
    Used to manage conversational state, correlate frontend and backend data, and persist conversations across EVI sessions.
    """

    data: str = pydantic.Field()
    """
    Base64 encoded audio input to insert into the conversation.
    
    The content of an Audio Input message is treated as the user’s speech to EVI and must be streamed continuously. Pre-recorded audio files are not supported.
    
    For optimal transcription quality, the audio data should be transmitted in small chunks.
    
    Hume recommends streaming audio with a buffer window of 20 milliseconds (ms), or 100 milliseconds (ms) for web applications.
    """

    type: typing.Literal["audio_input"] = pydantic.Field(default="audio_input")
    """
    The type of message sent through the socket; must be `audio_input` for our server to correctly identify and process it as an Audio Input message.
    
    This message is used for sending audio input data to EVI for processing and expression measurement. Audio data should be sent as a continuous stream, encoded in Base64.
    """

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
