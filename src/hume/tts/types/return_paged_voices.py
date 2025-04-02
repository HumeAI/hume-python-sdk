# This file was auto-generated by Fern from our API Definition.

from ...core.pydantic_utilities import UniversalBaseModel
import typing
from .return_voice import ReturnVoice
from ...core.pydantic_utilities import IS_PYDANTIC_V2
import pydantic


class ReturnPagedVoices(UniversalBaseModel):
    """
    A paginated list Octave voices available for text-to-speech
    """

    page_number: typing.Optional[int] = None
    page_size: typing.Optional[int] = None
    total_pages: typing.Optional[int] = None
    voices_page: typing.Optional[typing.List[ReturnVoice]] = None

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
