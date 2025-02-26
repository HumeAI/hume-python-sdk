# This file was auto-generated by Fern from our API Definition.

from ...core.pydantic_utilities import UniversalBaseModel
import typing
from .return_generation import ReturnGeneration
import pydantic
from ...core.pydantic_utilities import IS_PYDANTIC_V2


class ReturnTts(UniversalBaseModel):
    generations: typing.List[ReturnGeneration]
    request_id: typing.Optional[str] = pydantic.Field(default=None)
    """
    A unique ID associated with this request for tracking and troubleshooting. Use this ID when  contacting [support](/support) for troubleshooting assistance.
    """

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
