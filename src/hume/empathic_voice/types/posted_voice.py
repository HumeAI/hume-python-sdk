# This file was auto-generated by Fern from our API Definition.

from ...core.pydantic_utilities import UniversalBaseModel
from .posted_voice_provider import PostedVoiceProvider
import pydantic
import typing
from .posted_custom_voice import PostedCustomVoice
from ...core.pydantic_utilities import IS_PYDANTIC_V2


class PostedVoice(UniversalBaseModel):
    """
    A Voice specification posted to the server
    """

    provider: PostedVoiceProvider = pydantic.Field()
    """
    The provider of the voice to use. Supported values are `HUME_AI` and `CUSTOM_VOICE`.
    """

    name: typing.Optional[str] = pydantic.Field(default=None)
    """
    Specifies the name of the voice to use.
    
    This can be either the name of a previously created Custom Voice or one of our 8 base voices: `ITO`, `KORA`, `DACHER`, `AURA`, `FINN`, `WHIMSY`, `STELLA`, or `SUNNY`.
    
    The name will be automatically converted to uppercase (e.g., "Ito" becomes "ITO"). If a name is not specified, then a [Custom Voice](/reference/empathic-voice-interface-evi/configs/create-config#request.body.voice.custom_voice) specification must be provided.
    """

    custom_voice: typing.Optional[PostedCustomVoice] = None

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
