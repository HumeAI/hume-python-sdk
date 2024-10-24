# This file was auto-generated by Fern from our API Definition.

from ...core.pydantic_utilities import UniversalBaseModel
import typing
import pydantic
from .posted_custom_voice import PostedCustomVoice
from ...core.pydantic_utilities import IS_PYDANTIC_V2


class PostedVoice(UniversalBaseModel):
    """
    A Voice specification posted to the server
    """

    provider: typing.Literal["HUME_AI"] = pydantic.Field(default="HUME_AI")
    """
    The provider of the voice to use. Currently, only `HUME_AI` is supported as the voice provider.
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
