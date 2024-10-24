# This file was auto-generated by Fern from our API Definition.

from ...core.pydantic_utilities import UniversalBaseModel
import typing
import pydantic
from ...core.pydantic_utilities import IS_PYDANTIC_V2


class AssistantInput(UniversalBaseModel):
    """
    When provided, the input is spoken by EVI.
    """

    type: typing.Literal["assistant_input"] = pydantic.Field(default="assistant_input")
    """
    The type of message sent through the socket; must be `assistant_input` for our server to correctly identify and process it as an Assistant Input message.
    """

    custom_session_id: typing.Optional[str] = pydantic.Field(default=None)
    """
    Used to manage conversational state, correlate frontend and backend data, and persist conversations across EVI sessions.
    """

    text: str = pydantic.Field()
    """
    Assistant text to synthesize into spoken audio and insert into the conversation.
    
    EVI uses this text to generate spoken audio using our proprietary expressive text-to-speech model. Our model adds appropriate emotional inflections and tones to the text based on the user’s expressions and the context of the conversation. The synthesized audio is streamed back to the user as an [Assistant Message](/reference/empathic-voice-interface-evi/chat/chat#receive.Assistant%20Message.type).
    """

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow