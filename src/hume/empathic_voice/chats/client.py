# This file was auto-generated by Fern from our API Definition.

from ...core.client_wrapper import SyncClientWrapper
import typing
from ...core.request_options import RequestOptions
from ...core.pagination import SyncPager
from ..types.return_chat import ReturnChat
from ..types.return_paged_chats import ReturnPagedChats
from ...core.pydantic_utilities import parse_obj_as
from json.decoder import JSONDecodeError
from ...core.api_error import ApiError
from ..types.return_chat_event import ReturnChatEvent
from ...core.jsonable_encoder import jsonable_encoder
from ..types.return_chat_paged_events import ReturnChatPagedEvents
from ...core.client_wrapper import AsyncClientWrapper
from ...core.pagination import AsyncPager


class ChatsClient:
    def __init__(self, *, client_wrapper: SyncClientWrapper):
        self._client_wrapper = client_wrapper

    def list_chats(
        self,
        *,
        page_number: typing.Optional[int] = None,
        page_size: typing.Optional[int] = None,
        ascending_order: typing.Optional[bool] = None,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> SyncPager[ReturnChat]:
        """
        Parameters
        ----------
        page_number : typing.Optional[int]
            Specifies the page number to retrieve, enabling pagination.

            This parameter uses zero-based indexing. For example, setting `page_number` to 0 retrieves the first page of results (items 0-9 if `page_size` is 10), setting `page_number` to 1 retrieves the second page (items 10-19), and so on. Defaults to 0, which retrieves the first page.

        page_size : typing.Optional[int]
            Specifies the maximum number of results to include per page, enabling pagination. The value must be between 1 and 100, inclusive.

            For example, if `page_size` is set to 10, each page will include up to 10 items. Defaults to 10.

        ascending_order : typing.Optional[bool]
            Specifies the sorting order of the results based on their creation date. Set to true for ascending order (chronological, with the oldest records first) and false for descending order (reverse-chronological, with the newest records first). Defaults to true.

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        SyncPager[ReturnChat]
            Success

        Examples
        --------
        from hume import HumeClient

        client = HumeClient(
            api_key="YOUR_API_KEY",
        )
        response = client.empathic_voice.chats.list_chats(
            page_number=0,
            page_size=1,
            ascending_order=True,
        )
        for item in response:
            yield item
        # alternatively, you can paginate page-by-page
        for page in response.iter_pages():
            yield page
        """
        page_number = page_number if page_number is not None else 1
        _response = self._client_wrapper.httpx_client.request(
            "v0/evi/chats",
            method="GET",
            params={
                "page_number": page_number,
                "page_size": page_size,
                "ascending_order": ascending_order,
            },
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                _parsed_response = typing.cast(
                    ReturnPagedChats,
                    parse_obj_as(
                        type_=ReturnPagedChats,  # type: ignore
                        object_=_response.json(),
                    ),
                )
                _has_next = True
                _get_next = lambda: self.list_chats(
                    page_number=page_number + 1,
                    page_size=page_size,
                    ascending_order=ascending_order,
                    request_options=request_options,
                )
                _items = _parsed_response.chats_page
                return SyncPager(has_next=_has_next, items=_items, get_next=_get_next)
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def list_chat_events(
        self,
        id: str,
        *,
        page_size: typing.Optional[int] = None,
        page_number: typing.Optional[int] = None,
        ascending_order: typing.Optional[bool] = None,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> SyncPager[ReturnChatEvent]:
        """
        Parameters
        ----------
        id : str
            Identifier for a Chat. Formatted as a UUID.

        page_size : typing.Optional[int]
            Specifies the maximum number of results to include per page, enabling pagination. The value must be between 1 and 100, inclusive.

            For example, if `page_size` is set to 10, each page will include up to 10 items. Defaults to 10.

        page_number : typing.Optional[int]
            Specifies the page number to retrieve, enabling pagination.

            This parameter uses zero-based indexing. For example, setting `page_number` to 0 retrieves the first page of results (items 0-9 if `page_size` is 10), setting `page_number` to 1 retrieves the second page (items 10-19), and so on. Defaults to 0, which retrieves the first page.

        ascending_order : typing.Optional[bool]
            Specifies the sorting order of the results based on their creation date. Set to true for ascending order (chronological, with the oldest records first) and false for descending order (reverse-chronological, with the newest records first). Defaults to true.

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        SyncPager[ReturnChatEvent]
            Success

        Examples
        --------
        from hume import HumeClient

        client = HumeClient(
            api_key="YOUR_API_KEY",
        )
        response = client.empathic_voice.chats.list_chat_events(
            id="470a49f6-1dec-4afe-8b61-035d3b2d63b0",
            page_number=0,
            page_size=3,
            ascending_order=True,
        )
        for item in response:
            yield item
        # alternatively, you can paginate page-by-page
        for page in response.iter_pages():
            yield page
        """
        page_number = page_number if page_number is not None else 1
        _response = self._client_wrapper.httpx_client.request(
            f"v0/evi/chats/{jsonable_encoder(id)}",
            method="GET",
            params={
                "page_size": page_size,
                "page_number": page_number,
                "ascending_order": ascending_order,
            },
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                _parsed_response = typing.cast(
                    ReturnChatPagedEvents,
                    parse_obj_as(
                        type_=ReturnChatPagedEvents,  # type: ignore
                        object_=_response.json(),
                    ),
                )
                _has_next = True
                _get_next = lambda: self.list_chat_events(
                    id,
                    page_size=page_size,
                    page_number=page_number + 1,
                    ascending_order=ascending_order,
                    request_options=request_options,
                )
                _items = _parsed_response.events_page
                return SyncPager(has_next=_has_next, items=_items, get_next=_get_next)
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)


class AsyncChatsClient:
    def __init__(self, *, client_wrapper: AsyncClientWrapper):
        self._client_wrapper = client_wrapper

    async def list_chats(
        self,
        *,
        page_number: typing.Optional[int] = None,
        page_size: typing.Optional[int] = None,
        ascending_order: typing.Optional[bool] = None,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> AsyncPager[ReturnChat]:
        """
        Parameters
        ----------
        page_number : typing.Optional[int]
            Specifies the page number to retrieve, enabling pagination.

            This parameter uses zero-based indexing. For example, setting `page_number` to 0 retrieves the first page of results (items 0-9 if `page_size` is 10), setting `page_number` to 1 retrieves the second page (items 10-19), and so on. Defaults to 0, which retrieves the first page.

        page_size : typing.Optional[int]
            Specifies the maximum number of results to include per page, enabling pagination. The value must be between 1 and 100, inclusive.

            For example, if `page_size` is set to 10, each page will include up to 10 items. Defaults to 10.

        ascending_order : typing.Optional[bool]
            Specifies the sorting order of the results based on their creation date. Set to true for ascending order (chronological, with the oldest records first) and false for descending order (reverse-chronological, with the newest records first). Defaults to true.

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        AsyncPager[ReturnChat]
            Success

        Examples
        --------
        import asyncio

        from hume import AsyncHumeClient

        client = AsyncHumeClient(
            api_key="YOUR_API_KEY",
        )


        async def main() -> None:
            response = await client.empathic_voice.chats.list_chats(
                page_number=0,
                page_size=1,
                ascending_order=True,
            )
            async for item in response:
                yield item
            # alternatively, you can paginate page-by-page
            async for page in response.iter_pages():
                yield page


        asyncio.run(main())
        """
        page_number = page_number if page_number is not None else 1
        _response = await self._client_wrapper.httpx_client.request(
            "v0/evi/chats",
            method="GET",
            params={
                "page_number": page_number,
                "page_size": page_size,
                "ascending_order": ascending_order,
            },
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                _parsed_response = typing.cast(
                    ReturnPagedChats,
                    parse_obj_as(
                        type_=ReturnPagedChats,  # type: ignore
                        object_=_response.json(),
                    ),
                )
                _has_next = True
                _get_next = lambda: self.list_chats(
                    page_number=page_number + 1,
                    page_size=page_size,
                    ascending_order=ascending_order,
                    request_options=request_options,
                )
                _items = _parsed_response.chats_page
                return AsyncPager(has_next=_has_next, items=_items, get_next=_get_next)
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    async def list_chat_events(
        self,
        id: str,
        *,
        page_size: typing.Optional[int] = None,
        page_number: typing.Optional[int] = None,
        ascending_order: typing.Optional[bool] = None,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> AsyncPager[ReturnChatEvent]:
        """
        Parameters
        ----------
        id : str
            Identifier for a Chat. Formatted as a UUID.

        page_size : typing.Optional[int]
            Specifies the maximum number of results to include per page, enabling pagination. The value must be between 1 and 100, inclusive.

            For example, if `page_size` is set to 10, each page will include up to 10 items. Defaults to 10.

        page_number : typing.Optional[int]
            Specifies the page number to retrieve, enabling pagination.

            This parameter uses zero-based indexing. For example, setting `page_number` to 0 retrieves the first page of results (items 0-9 if `page_size` is 10), setting `page_number` to 1 retrieves the second page (items 10-19), and so on. Defaults to 0, which retrieves the first page.

        ascending_order : typing.Optional[bool]
            Specifies the sorting order of the results based on their creation date. Set to true for ascending order (chronological, with the oldest records first) and false for descending order (reverse-chronological, with the newest records first). Defaults to true.

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        AsyncPager[ReturnChatEvent]
            Success

        Examples
        --------
        import asyncio

        from hume import AsyncHumeClient

        client = AsyncHumeClient(
            api_key="YOUR_API_KEY",
        )


        async def main() -> None:
            response = await client.empathic_voice.chats.list_chat_events(
                id="470a49f6-1dec-4afe-8b61-035d3b2d63b0",
                page_number=0,
                page_size=3,
                ascending_order=True,
            )
            async for item in response:
                yield item
            # alternatively, you can paginate page-by-page
            async for page in response.iter_pages():
                yield page


        asyncio.run(main())
        """
        page_number = page_number if page_number is not None else 1
        _response = await self._client_wrapper.httpx_client.request(
            f"v0/evi/chats/{jsonable_encoder(id)}",
            method="GET",
            params={
                "page_size": page_size,
                "page_number": page_number,
                "ascending_order": ascending_order,
            },
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                _parsed_response = typing.cast(
                    ReturnChatPagedEvents,
                    parse_obj_as(
                        type_=ReturnChatPagedEvents,  # type: ignore
                        object_=_response.json(),
                    ),
                )
                _has_next = True
                _get_next = lambda: self.list_chat_events(
                    id,
                    page_size=page_size,
                    page_number=page_number + 1,
                    ascending_order=ascending_order,
                    request_options=request_options,
                )
                _items = _parsed_response.events_page
                return AsyncPager(has_next=_has_next, items=_items, get_next=_get_next)
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)
