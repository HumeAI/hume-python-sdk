# This file was auto-generated by Fern from our API Definition.

import datetime as dt
import typing

from ...core.datetime_utils import serialize_datetime
from ...core.pydantic_utilities import deep_union_pydantic_dicts, pydantic_v1
from .return_chat import ReturnChat


class ReturnChatGroupPagedChats(pydantic_v1.BaseModel):
    """
    A description of chat_group and its status with a paginated list of each chat in the chat_group
    """

    id: str = pydantic_v1.Field()
    """
    Identifier for the chat group. Any chat resumed from this chat will have the same chat_group_id. Formatted as a UUID.
    """

    first_start_timestamp: int = pydantic_v1.Field()
    """
    The timestamp when the first chat in this chat group started, formatted as a Unix epoch milliseconds.
    """

    most_recent_start_timestamp: int = pydantic_v1.Field()
    """
    The timestamp when the most recent chat in this chat group started, formatted as a Unix epoch milliseconds.
    """

    num_chats: int = pydantic_v1.Field()
    """
    The total number of chats in this chat group.
    """

    page_number: int = pydantic_v1.Field()
    """
    The page number of the returned results.
    """

    page_size: int = pydantic_v1.Field()
    """
    The number of results returned per page.
    """

    chats_page: typing.List[ReturnChat] = pydantic_v1.Field()
    """
    List of chats and their metadata returned for the specified page number and page size.
    """

    active: typing.Optional[bool] = None

    def json(self, **kwargs: typing.Any) -> str:
        kwargs_with_defaults: typing.Any = {"by_alias": True, "exclude_unset": True, **kwargs}
        return super().json(**kwargs_with_defaults)

    def dict(self, **kwargs: typing.Any) -> typing.Dict[str, typing.Any]:
        kwargs_with_defaults_exclude_unset: typing.Any = {"by_alias": True, "exclude_unset": True, **kwargs}
        kwargs_with_defaults_exclude_none: typing.Any = {"by_alias": True, "exclude_none": True, **kwargs}

        return deep_union_pydantic_dicts(
            super().dict(**kwargs_with_defaults_exclude_unset), super().dict(**kwargs_with_defaults_exclude_none)
        )

    class Config:
        frozen = True
        smart_union = True
        extra = pydantic_v1.Extra.allow
        json_encoders = {dt.datetime: serialize_datetime}