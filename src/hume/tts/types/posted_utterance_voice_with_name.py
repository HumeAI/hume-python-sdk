# This file was auto-generated by Fern from our API Definition.

import typing

import pydantic
from ...core.pydantic_utilities import IS_PYDANTIC_V2, UniversalBaseModel
from .voice_provider import VoiceProvider


class PostedUtteranceVoiceWithName(UniversalBaseModel):
    name: str = pydantic.Field()
    """
    The name of a **Voice**.
    """

    provider: typing.Optional[VoiceProvider] = pydantic.Field(default=None)
    """
    Specifies the source provider associated with the chosen voice.
    
    - **`HUME_AI`**: Select voices from Hume's [Voice Library](https://platform.hume.ai/tts/voice-library), containing a variety of preset, shared voices.
    - **`CUSTOM_VOICE`**: Select from voices you've personally generated and saved in your account. 
    
    If no provider is explicitly set, the default provider is `CUSTOM_VOICE`. When using voices from Hume's **Voice Library**, you must explicitly set the provider to `HUME_AI`.
    
    Preset voices from Hume's **Voice Library** are accessible by all users. In contrast, your custom voices are private and accessible only via requests authenticated with your API key.
    """

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
