# This file was auto-generated by Fern from our API Definition.

from ...core.pydantic_utilities import UniversalBaseModel
import typing_extensions
import typing
from ...core.serialization import FieldMetadata
from .voice_args import VoiceArgs
from ...core.pydantic_utilities import IS_PYDANTIC_V2
import pydantic


class ExtendedVoiceArgs(UniversalBaseModel):
    text: str
    use_s_2_a: typing_extensions.Annotated[typing.Optional[bool], FieldMetadata(alias="use_s2a")] = None
    voice_args: VoiceArgs

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
