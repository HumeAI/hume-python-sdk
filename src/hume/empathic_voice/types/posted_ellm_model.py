# This file was auto-generated by Fern from our API Definition.

from ...core.pydantic_utilities import UniversalBaseModel
import typing
import pydantic
from ...core.pydantic_utilities import IS_PYDANTIC_V2


class PostedEllmModel(UniversalBaseModel):
    """
    A eLLM model configuration to be posted to the server
    """

    allow_short_responses: typing.Optional[bool] = pydantic.Field(default=None)
    """
    Boolean indicating if the eLLM is allowed to generate short responses.
    
    If omitted, short responses from the eLLM are enabled by default.
    """

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
