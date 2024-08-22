# This file was auto-generated by Fern from our API Definition.

from ...core.pydantic_utilities import UniversalBaseModel
import pydantic
import typing
from .return_user_defined_tool import ReturnUserDefinedTool
from ...core.pydantic_utilities import IS_PYDANTIC_V2


class ReturnPagedUserDefinedTools(UniversalBaseModel):
    """
    A paginated list of user defined tool versions returned from the server
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

    tools_page: typing.List[typing.Optional[ReturnUserDefinedTool]] = pydantic.Field()
    """
    List of tools returned for the specified `page_number` and `page_size`.
    """

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
