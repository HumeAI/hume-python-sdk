# This file was auto-generated by Fern from our API Definition.

from ...core.pydantic_utilities import UniversalBaseModel
import typing
from .posted_context import PostedContext
import pydantic
from .format import Format
from .posted_utterance import PostedUtterance
from ...core.pydantic_utilities import IS_PYDANTIC_V2


class PostedTts(UniversalBaseModel):
    context: typing.Optional[PostedContext] = pydantic.Field(default=None)
    """
    Utterances to use as context for generating consistent speech style and prosody across multiple requests. These will not be converted to speech output.
    """

    format: typing.Optional[Format] = pydantic.Field(default=None)
    """
    Specifies the output audio file format.
    """

    num_generations: typing.Optional[int] = pydantic.Field(default=None)
    """
    Number of generations of the audio to produce.
    """

    split_utterances: typing.Optional[bool] = pydantic.Field(default=None)
    """
    Controls how audio output is segmented in the response.
    
    - When **enabled** (`true`),  input utterances are automatically split into natural-sounding speech segments.
    
    - When **disabled**  (`false`), the response maintains a strict one-to-one mapping between input utterances and output snippets. 
    
    This setting affects how the `snippets` array is structured in the response, which may be important  for applications that need to track the relationship between input text and generated audio segments. When  setting to `false`, avoid including utterances with long `text`, as this can result in distorted output.
    """

    utterances: typing.List[PostedUtterance] = pydantic.Field()
    """
    A list of **Utterances** to be converted to speech output.
    
    An **Utterance** is a unit of  input for [Octave](/docs/text-to-speech-tts/overview), and includes input `text`, an  optional `description` to serve as the prompt for how the speech should be delivered, an optional `voice` specification, and additional controls to guide delivery for `speed` and `trailing_silence`.
    """

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
