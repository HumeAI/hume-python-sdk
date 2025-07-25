# This file was auto-generated by Fern from our API Definition.

import typing

import pydantic
from ....core.pydantic_utilities import IS_PYDANTIC_V2, UniversalBaseModel


class TimeInterval(UniversalBaseModel):
    """
    A time range with a beginning and end, measured in seconds.
    """

    begin: float = pydantic.Field()
    """
    Beginning of time range in seconds.
    """

    end: float = pydantic.Field()
    """
    End of time range in seconds.
    """

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
