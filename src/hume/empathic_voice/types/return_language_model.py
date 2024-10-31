# This file was auto-generated by Fern from our API Definition.

from ...core.pydantic_utilities import UniversalBaseModel
import typing
from .return_language_model_model_provider import ReturnLanguageModelModelProvider
import pydantic
from .return_language_model_model_resource import ReturnLanguageModelModelResource
from ...core.pydantic_utilities import IS_PYDANTIC_V2


class ReturnLanguageModel(UniversalBaseModel):
    """
    A specific LanguageModel
    """

    model_provider: typing.Optional[ReturnLanguageModelModelProvider] = pydantic.Field(default=None)
    """
    The provider of the supplemental language model.
    """

    model_resource: typing.Optional[ReturnLanguageModelModelResource] = pydantic.Field(default=None)
    """
    String that specifies the language model to use with `model_provider`.
    """

    temperature: typing.Optional[float] = pydantic.Field(default=None)
    """
    The model temperature, with values between 0 to 1 (inclusive).
    
    Controls the randomness of the LLM’s output, with values closer to 0 yielding focused, deterministic responses and values closer to 1 producing more creative, diverse responses.
    """

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
