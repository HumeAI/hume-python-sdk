# This file was auto-generated by Fern from our API Definition.

from ...core.pydantic_utilities import UniversalBaseModel
import typing
from .context import Context
import pydantic
from .format import Format
from .posted_utterance import PostedUtterance
from ...core.pydantic_utilities import IS_PYDANTIC_V2


class OctaveBodyArgsFile(UniversalBaseModel):
    context: typing.Optional[Context] = pydantic.Field(default=None)
    """
    Utterances to use as context for generating consistent speech style and prosody across multiple requests. These will not be converted to speech output.
    """

    expand_description: typing.Optional[bool] = pydantic.Field(default=None)
    """
    If enabled, enhances the provided description prompt to improve voice generation quality.
    """

    filter_generations: typing.Optional[bool] = pydantic.Field(default=None)
    """
    If enabled, additional generations will be made, and the best `num_generations` of them all will be returned.
    """

    format: typing.Optional[Format] = None
    model: typing.Optional[typing.Literal["octave"]] = pydantic.Field(default=None)
    """
    The TTS model to use for speech generations.
    """

    split_utterances: typing.Optional[bool] = pydantic.Field(default=None)
    """
    If enabled, each input utterance will be split as needed into more natural-sounding `snippets` of speech for audio generation.
    """

    utterances: typing.List[PostedUtterance] = pydantic.Field()
    """
    Utterances to be converted to speech output.
    """

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
