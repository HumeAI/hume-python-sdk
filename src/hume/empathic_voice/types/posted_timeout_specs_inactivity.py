# This file was auto-generated by Fern from our API Definition.

from ...core.pydantic_utilities import UniversalBaseModel
import pydantic
import typing
from ...core.pydantic_utilities import IS_PYDANTIC_V2


class PostedTimeoutSpecsInactivity(UniversalBaseModel):
    """
    Specifies the duration of user inactivity (in seconds) after which the EVI WebSocket connection will be automatically disconnected. Default is 600 seconds (10 minutes).

    Accepts a minimum value of 30 seconds and a maximum value of 1,800 seconds.
    """

    enabled: bool = pydantic.Field()
    """
    Boolean indicating if this timeout is enabled.
    
    If set to false, EVI will not timeout due to a specified duration of user inactivity being reached. However, the conversation will eventually disconnect after 1,800 seconds (30 minutes), which is the maximum WebSocket duration limit for EVI.
    """

    duration_secs: typing.Optional[int] = pydantic.Field(default=None)
    """
    Duration in seconds for the timeout (e.g. 600 seconds represents 10 minutes).
    """

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
