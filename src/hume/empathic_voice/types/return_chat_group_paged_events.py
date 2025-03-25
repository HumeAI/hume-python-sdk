# This file was auto-generated by Fern from our API Definition.

from ...core.pydantic_utilities import UniversalBaseModel
import pydantic
from .return_chat_group_paged_events_pagination_direction import ReturnChatGroupPagedEventsPaginationDirection
import typing
from .return_chat_event import ReturnChatEvent
from ...core.pydantic_utilities import IS_PYDANTIC_V2


class ReturnChatGroupPagedEvents(UniversalBaseModel):
    """
    A paginated list of chat events that occurred across chats in this chat_group from the server
    """

    id: str = pydantic.Field()
    """
    Identifier for the Chat Group. Any Chat resumed from this Chat Group will have the same `chat_group_id`. Formatted as a UUID.
    """

    page_number: int = pydantic.Field()
    """
    The page number of the returned list.
    
    This value corresponds to the `page_number` parameter specified in the request. Pagination uses zero-based indexing.
    """

    page_size: int = pydantic.Field()
    """
    The maximum number of items returned per page.
    
    This value corresponds to the `page_size` parameter specified in the request.
    """

    total_pages: int = pydantic.Field()
    """
    The total number of pages in the collection.
    """

    pagination_direction: ReturnChatGroupPagedEventsPaginationDirection = pydantic.Field()
    """
    Indicates the order in which the paginated results are presented, based on their creation date.
    
    It shows `ASC` for ascending order (chronological, with the oldest records first) or `DESC` for descending order (reverse-chronological, with the newest records first). This value corresponds to the `ascending_order` query parameter used in the request.
    """

    events_page: typing.List[ReturnChatEvent] = pydantic.Field()
    """
    List of Chat Events for the specified `page_number` and `page_size`.
    """

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
