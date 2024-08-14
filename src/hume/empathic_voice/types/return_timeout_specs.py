# This file was auto-generated by Fern from our API Definition.

from ...core.pydantic_utilities import UniversalBaseModel
from .return_timeout_spec import ReturnTimeoutSpec
import pydantic
from ...core.pydantic_utilities import IS_PYDANTIC_V2
import typing


class ReturnTimeoutSpecs(UniversalBaseModel):
    """
    Collection of timeout specifications returned by the server.

    Timeouts are sent by the server when specific time-based events occur during a chat session. These specifications set the inactivity timeout and the maximum duration an EVI WebSocket connection can stay open before it is automatically disconnected.
    """

    inactivity: ReturnTimeoutSpec = pydantic.Field()
    """
    Specifies the duration of user inactivity (in seconds) after which the EVI WebSocket connection will be automatically disconnected. Default is 600 seconds (10 minutes).
    
    Accepts a minimum value of 1 second and a maximum value of 1,800 seconds.
    """

    max_duration: ReturnTimeoutSpec = pydantic.Field()
    """
    Specifies the maximum allowed duration (in seconds) for an EVI WebSocket connection before it is automatically disconnected. Default is 1,800 seconds (30 minutes).
    
    Accepts a minimum value of 1 second and a maximum value of 1,800 seconds.
    """

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
