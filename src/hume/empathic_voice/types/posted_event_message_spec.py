# This file was auto-generated by Fern from our API Definition.

from ...core.pydantic_utilities import UniversalBaseModel
import pydantic
import typing
from ...core.pydantic_utilities import IS_PYDANTIC_V2


class PostedEventMessageSpec(UniversalBaseModel):
    """
    Settings for a specific event_message to be posted to the server
    """

    enabled: bool = pydantic.Field()
    """
    Boolean indicating if this event message is enabled.
    
    If set to `true`, a message will be sent when the circumstances for the specific event are met.
    """

    text: typing.Optional[str] = pydantic.Field(default=None)
    """
    Text to use as the event message when the corresponding event occurs. If no text is specified, EVI will generate an appropriate message based on its current context and the system prompt.
    """

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
