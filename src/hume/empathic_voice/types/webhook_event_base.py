# This file was auto-generated by Fern from our API Definition.

import typing

import pydantic
from ...core.pydantic_utilities import IS_PYDANTIC_V2, UniversalBaseModel


class WebhookEventBase(UniversalBaseModel):
    """
    Represents the fields common to all webhook events.
    """

    chat_group_id: str = pydantic.Field()
    """
    Unique ID of the **Chat Group** associated with the **Chat** session.
    """

    chat_id: str = pydantic.Field()
    """
    Unique ID of the **Chat** session.
    """

    config_id: typing.Optional[str] = pydantic.Field(default=None)
    """
    Unique ID of the EVI **Config** used for the session.
    """

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
