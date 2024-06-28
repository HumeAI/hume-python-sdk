# This file was auto-generated by Fern from our API Definition.

import typing
from json.decoder import JSONDecodeError

from ...core.api_error import ApiError
from ...core.client_wrapper import AsyncClientWrapper, SyncClientWrapper
from ...core.jsonable_encoder import jsonable_encoder
from ...core.pagination import AsyncPager, SyncPager
from ...core.pydantic_utilities import pydantic_v1
from ...core.request_options import RequestOptions
from ..types.return_paged_user_defined_tools import ReturnPagedUserDefinedTools
from ..types.return_user_defined_tool import ReturnUserDefinedTool

# this is used as the default value for optional parameters
OMIT = typing.cast(typing.Any, ...)


class ToolsClient:
    def __init__(self, *, client_wrapper: SyncClientWrapper):
        self._client_wrapper = client_wrapper

    def list_tools(
        self,
        *,
        page_number: typing.Optional[int] = None,
        page_size: typing.Optional[int] = None,
        restrict_to_most_recent: typing.Optional[bool] = None,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> SyncPager[typing.Optional[ReturnUserDefinedTool]]:
        """
        Parameters
        ----------
        page_number : typing.Optional[int]
            The page number of the results to return.

        page_size : typing.Optional[int]
            The maximum number of results to include per page.

        restrict_to_most_recent : typing.Optional[bool]
            Only include the most recent version of each tool in the list.

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        SyncPager[typing.Optional[ReturnUserDefinedTool]]
            Success

        Examples
        --------
        from hume.client import HumeClient

        client = HumeClient(
            api_key="YOUR_API_KEY",
        )
        client.empathic_voice.tools.list_tools(
            page_number=0,
            page_size=2,
        )
        """
        _response = self._client_wrapper.httpx_client.request(
            "v0/evi/tools",
            method="GET",
            params={
                "page_number": page_number,
                "page_size": page_size,
                "restrict_to_most_recent": restrict_to_most_recent,
            },
            request_options=request_options,
        )
        if 200 <= _response.status_code < 300:
            _parsed_response = pydantic_v1.parse_obj_as(ReturnPagedUserDefinedTools, _response.json())  # type: ignore
            _has_next = True
            _get_next = lambda: self.list_tools(
                page_number=page_number + 1 if page_number is not None else 1,
                page_size=page_size,
                restrict_to_most_recent=restrict_to_most_recent,
                request_options=request_options,
            )
            _items = _parsed_response.tools_page
            return SyncPager(has_next=_has_next, items=_items, get_next=_get_next)
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def create_tool(
        self,
        *,
        name: str,
        parameters: str,
        version_description: typing.Optional[str] = OMIT,
        description: typing.Optional[str] = OMIT,
        fallback_content: typing.Optional[str] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> typing.Optional[ReturnUserDefinedTool]:
        """
        Parameters
        ----------
        name : str
            Name applied to all versions of a particular Tool.

        parameters : str
            Stringified JSON defining the parameters used by this version of the Tool.

        version_description : typing.Optional[str]
            Description that is appended to a specific version of a Tool.

        description : typing.Optional[str]
            Text describing what the tool does.

        fallback_content : typing.Optional[str]
            Text to use if the tool fails to generate content.

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        typing.Optional[ReturnUserDefinedTool]
            Success

        Examples
        --------
        from hume.client import HumeClient

        client = HumeClient(
            api_key="YOUR_API_KEY",
        )
        client.empathic_voice.tools.create_tool(
            name="get_current_weather",
            parameters='{ "type": "object", "properties": { "location": { "type": "string", "description": "The city and state, e.g. San Francisco, CA" }, "format": { "type": "string", "enum": ["celsius", "fahrenheit"], "description": "The temperature unit to use. Infer this from the users location." } }, "required": ["location", "format"] }',
            version_description="Fetches current weather and uses celsius or fahrenheit based on location of user.",
            description="This tool is for getting the current weather.",
            fallback_content="Unable to fetch current weather.",
        )
        """
        _response = self._client_wrapper.httpx_client.request(
            "v0/evi/tools",
            method="POST",
            json={
                "name": name,
                "version_description": version_description,
                "description": description,
                "parameters": parameters,
                "fallback_content": fallback_content,
            },
            request_options=request_options,
            omit=OMIT,
        )
        if 200 <= _response.status_code < 300:
            return pydantic_v1.parse_obj_as(typing.Optional[ReturnUserDefinedTool], _response.json())  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def list_tool_versions(
        self,
        id: str,
        *,
        page_number: typing.Optional[int] = None,
        page_size: typing.Optional[int] = None,
        restrict_to_most_recent: typing.Optional[bool] = None,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> ReturnPagedUserDefinedTools:
        """
        Parameters
        ----------
        id : str
            Identifier for a tool. Formatted as a UUID.

        page_number : typing.Optional[int]
            The page number of the results to return.

        page_size : typing.Optional[int]
            The maximum number of results to include per page.

        restrict_to_most_recent : typing.Optional[bool]
            Only include the most recent version of each tool in the list.

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        ReturnPagedUserDefinedTools
            Success

        Examples
        --------
        from hume.client import HumeClient

        client = HumeClient(
            api_key="YOUR_API_KEY",
        )
        client.empathic_voice.tools.list_tool_versions(
            id="00183a3f-79ba-413d-9f3b-609864268bea",
        )
        """
        _response = self._client_wrapper.httpx_client.request(
            f"v0/evi/tools/{jsonable_encoder(id)}",
            method="GET",
            params={
                "page_number": page_number,
                "page_size": page_size,
                "restrict_to_most_recent": restrict_to_most_recent,
            },
            request_options=request_options,
        )
        if 200 <= _response.status_code < 300:
            return pydantic_v1.parse_obj_as(ReturnPagedUserDefinedTools, _response.json())  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def create_tool_version(
        self,
        id: str,
        *,
        parameters: str,
        version_description: typing.Optional[str] = OMIT,
        description: typing.Optional[str] = OMIT,
        fallback_content: typing.Optional[str] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> typing.Optional[ReturnUserDefinedTool]:
        """
        Parameters
        ----------
        id : str
            Identifier for a tool. Formatted as a UUID.

        parameters : str
            Stringified JSON defining the parameters used by this version of the Tool.

        version_description : typing.Optional[str]
            Description that is appended to a specific version of a Tool.

        description : typing.Optional[str]
            Text describing what the tool does.

        fallback_content : typing.Optional[str]
            Text to use if the tool fails to generate content.

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        typing.Optional[ReturnUserDefinedTool]
            Success

        Examples
        --------
        from hume.client import HumeClient

        client = HumeClient(
            api_key="YOUR_API_KEY",
        )
        client.empathic_voice.tools.create_tool_version(
            id="00183a3f-79ba-413d-9f3b-609864268bea",
            parameters='{ "type": "object", "properties": { "location": { "type": "string", "description": "The city and state, e.g. San Francisco, CA" }, "format": { "type": "string", "enum": ["celsius", "fahrenheit", "kelvin"], "description": "The temperature unit to use. Infer this from the users location." } }, "required": ["location", "format"] }',
            version_description="Fetches current weather and uses celsius, fahrenheit, or kelvin based on location of user.",
            fallback_content="Unable to fetch current weather.",
            description="This tool is for getting the current weather.",
        )
        """
        _response = self._client_wrapper.httpx_client.request(
            f"v0/evi/tools/{jsonable_encoder(id)}",
            method="POST",
            json={
                "version_description": version_description,
                "description": description,
                "parameters": parameters,
                "fallback_content": fallback_content,
            },
            request_options=request_options,
            omit=OMIT,
        )
        if 200 <= _response.status_code < 300:
            return pydantic_v1.parse_obj_as(typing.Optional[ReturnUserDefinedTool], _response.json())  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def delete_tool(self, id: str, *, request_options: typing.Optional[RequestOptions] = None) -> None:
        """
        Parameters
        ----------
        id : str
            Identifier for a tool. Formatted as a UUID.

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        None

        Examples
        --------
        from hume.client import HumeClient

        client = HumeClient(
            api_key="YOUR_API_KEY",
        )
        client.empathic_voice.tools.delete_tool(
            id="00183a3f-79ba-413d-9f3b-609864268bea",
        )
        """
        _response = self._client_wrapper.httpx_client.request(
            f"v0/evi/tools/{jsonable_encoder(id)}", method="DELETE", request_options=request_options
        )
        if 200 <= _response.status_code < 300:
            return
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def update_tool_name(self, id: str, *, name: str, request_options: typing.Optional[RequestOptions] = None) -> str:
        """
        Parameters
        ----------
        id : str
            Identifier for a tool. Formatted as a UUID.

        name : str
            Name applied to all versions of a particular Tool.

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        str
            Success

        Examples
        --------
        from hume.client import HumeClient

        client = HumeClient(
            api_key="YOUR_API_KEY",
        )
        client.empathic_voice.tools.update_tool_name(
            id="00183a3f-79ba-413d-9f3b-609864268bea",
            name="get_current_temperature",
        )
        """
        _response = self._client_wrapper.httpx_client.request(
            f"v0/evi/tools/{jsonable_encoder(id)}",
            method="PATCH",
            json={"name": name},
            request_options=request_options,
            omit=OMIT,
        )
        if 200 <= _response.status_code < 300:
            return _response.text  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def get_tool_version(
        self, id: str, version: int, *, request_options: typing.Optional[RequestOptions] = None
    ) -> typing.Optional[ReturnUserDefinedTool]:
        """
        Parameters
        ----------
        id : str
            Identifier for a tool. Formatted as a UUID.

        version : int
            Version number for a tool. Version numbers should be integers.

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        typing.Optional[ReturnUserDefinedTool]
            Success

        Examples
        --------
        from hume.client import HumeClient

        client = HumeClient(
            api_key="YOUR_API_KEY",
        )
        client.empathic_voice.tools.get_tool_version(
            id="00183a3f-79ba-413d-9f3b-609864268bea",
            version=1,
        )
        """
        _response = self._client_wrapper.httpx_client.request(
            f"v0/evi/tools/{jsonable_encoder(id)}/version/{jsonable_encoder(version)}",
            method="GET",
            request_options=request_options,
        )
        if 200 <= _response.status_code < 300:
            return pydantic_v1.parse_obj_as(typing.Optional[ReturnUserDefinedTool], _response.json())  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def delete_tool_version(
        self, id: str, version: int, *, request_options: typing.Optional[RequestOptions] = None
    ) -> None:
        """
        Parameters
        ----------
        id : str
            Identifier for a tool. Formatted as a UUID.

        version : int
            Version number for a tool. Version numbers should be integers.

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        None

        Examples
        --------
        from hume.client import HumeClient

        client = HumeClient(
            api_key="YOUR_API_KEY",
        )
        client.empathic_voice.tools.delete_tool_version(
            id="00183a3f-79ba-413d-9f3b-609864268bea",
            version=1,
        )
        """
        _response = self._client_wrapper.httpx_client.request(
            f"v0/evi/tools/{jsonable_encoder(id)}/version/{jsonable_encoder(version)}",
            method="DELETE",
            request_options=request_options,
        )
        if 200 <= _response.status_code < 300:
            return
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def update_tool_description(
        self,
        id: str,
        version: int,
        *,
        version_description: typing.Optional[str] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> typing.Optional[ReturnUserDefinedTool]:
        """
        Parameters
        ----------
        id : str
            Identifier for a tool. Formatted as a UUID.

        version : int
            Version number for a tool. Version numbers should be integers.

        version_description : typing.Optional[str]
            Description that is appended to a specific version of a Tool.

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        typing.Optional[ReturnUserDefinedTool]
            Success

        Examples
        --------
        from hume.client import HumeClient

        client = HumeClient(
            api_key="YOUR_API_KEY",
        )
        client.empathic_voice.tools.update_tool_description(
            id="00183a3f-79ba-413d-9f3b-609864268bea",
            version=1,
            version_description="Fetches current temperature, precipitation, wind speed, AQI, and other weather conditions. Uses Celsius, Fahrenheit, or kelvin depending on user's region.",
        )
        """
        _response = self._client_wrapper.httpx_client.request(
            f"v0/evi/tools/{jsonable_encoder(id)}/version/{jsonable_encoder(version)}",
            method="PATCH",
            json={"version_description": version_description},
            request_options=request_options,
            omit=OMIT,
        )
        if 200 <= _response.status_code < 300:
            return pydantic_v1.parse_obj_as(typing.Optional[ReturnUserDefinedTool], _response.json())  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)


class AsyncToolsClient:
    def __init__(self, *, client_wrapper: AsyncClientWrapper):
        self._client_wrapper = client_wrapper

    async def list_tools(
        self,
        *,
        page_number: typing.Optional[int] = None,
        page_size: typing.Optional[int] = None,
        restrict_to_most_recent: typing.Optional[bool] = None,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> AsyncPager[typing.Optional[ReturnUserDefinedTool]]:
        """
        Parameters
        ----------
        page_number : typing.Optional[int]
            The page number of the results to return.

        page_size : typing.Optional[int]
            The maximum number of results to include per page.

        restrict_to_most_recent : typing.Optional[bool]
            Only include the most recent version of each tool in the list.

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        AsyncPager[typing.Optional[ReturnUserDefinedTool]]
            Success

        Examples
        --------
        from hume.client import AsyncHumeClient

        client = AsyncHumeClient(
            api_key="YOUR_API_KEY",
        )
        await client.empathic_voice.tools.list_tools(
            page_number=0,
            page_size=2,
        )
        """
        _response = await self._client_wrapper.httpx_client.request(
            "v0/evi/tools",
            method="GET",
            params={
                "page_number": page_number,
                "page_size": page_size,
                "restrict_to_most_recent": restrict_to_most_recent,
            },
            request_options=request_options,
        )
        if 200 <= _response.status_code < 300:
            _parsed_response = pydantic_v1.parse_obj_as(ReturnPagedUserDefinedTools, _response.json())  # type: ignore
            _has_next = True
            _get_next = lambda: self.list_tools(
                page_number=page_number + 1 if page_number is not None else 1,
                page_size=page_size,
                restrict_to_most_recent=restrict_to_most_recent,
                request_options=request_options,
            )
            _items = _parsed_response.tools_page
            return AsyncPager(has_next=_has_next, items=_items, get_next=_get_next)
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    async def create_tool(
        self,
        *,
        name: str,
        parameters: str,
        version_description: typing.Optional[str] = OMIT,
        description: typing.Optional[str] = OMIT,
        fallback_content: typing.Optional[str] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> typing.Optional[ReturnUserDefinedTool]:
        """
        Parameters
        ----------
        name : str
            Name applied to all versions of a particular Tool.

        parameters : str
            Stringified JSON defining the parameters used by this version of the Tool.

        version_description : typing.Optional[str]
            Description that is appended to a specific version of a Tool.

        description : typing.Optional[str]
            Text describing what the tool does.

        fallback_content : typing.Optional[str]
            Text to use if the tool fails to generate content.

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        typing.Optional[ReturnUserDefinedTool]
            Success

        Examples
        --------
        from hume.client import AsyncHumeClient

        client = AsyncHumeClient(
            api_key="YOUR_API_KEY",
        )
        await client.empathic_voice.tools.create_tool(
            name="get_current_weather",
            parameters='{ "type": "object", "properties": { "location": { "type": "string", "description": "The city and state, e.g. San Francisco, CA" }, "format": { "type": "string", "enum": ["celsius", "fahrenheit"], "description": "The temperature unit to use. Infer this from the users location." } }, "required": ["location", "format"] }',
            version_description="Fetches current weather and uses celsius or fahrenheit based on location of user.",
            description="This tool is for getting the current weather.",
            fallback_content="Unable to fetch current weather.",
        )
        """
        _response = await self._client_wrapper.httpx_client.request(
            "v0/evi/tools",
            method="POST",
            json={
                "name": name,
                "version_description": version_description,
                "description": description,
                "parameters": parameters,
                "fallback_content": fallback_content,
            },
            request_options=request_options,
            omit=OMIT,
        )
        if 200 <= _response.status_code < 300:
            return pydantic_v1.parse_obj_as(typing.Optional[ReturnUserDefinedTool], _response.json())  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    async def list_tool_versions(
        self,
        id: str,
        *,
        page_number: typing.Optional[int] = None,
        page_size: typing.Optional[int] = None,
        restrict_to_most_recent: typing.Optional[bool] = None,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> ReturnPagedUserDefinedTools:
        """
        Parameters
        ----------
        id : str
            Identifier for a tool. Formatted as a UUID.

        page_number : typing.Optional[int]
            The page number of the results to return.

        page_size : typing.Optional[int]
            The maximum number of results to include per page.

        restrict_to_most_recent : typing.Optional[bool]
            Only include the most recent version of each tool in the list.

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        ReturnPagedUserDefinedTools
            Success

        Examples
        --------
        from hume.client import AsyncHumeClient

        client = AsyncHumeClient(
            api_key="YOUR_API_KEY",
        )
        await client.empathic_voice.tools.list_tool_versions(
            id="00183a3f-79ba-413d-9f3b-609864268bea",
        )
        """
        _response = await self._client_wrapper.httpx_client.request(
            f"v0/evi/tools/{jsonable_encoder(id)}",
            method="GET",
            params={
                "page_number": page_number,
                "page_size": page_size,
                "restrict_to_most_recent": restrict_to_most_recent,
            },
            request_options=request_options,
        )
        if 200 <= _response.status_code < 300:
            return pydantic_v1.parse_obj_as(ReturnPagedUserDefinedTools, _response.json())  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    async def create_tool_version(
        self,
        id: str,
        *,
        parameters: str,
        version_description: typing.Optional[str] = OMIT,
        description: typing.Optional[str] = OMIT,
        fallback_content: typing.Optional[str] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> typing.Optional[ReturnUserDefinedTool]:
        """
        Parameters
        ----------
        id : str
            Identifier for a tool. Formatted as a UUID.

        parameters : str
            Stringified JSON defining the parameters used by this version of the Tool.

        version_description : typing.Optional[str]
            Description that is appended to a specific version of a Tool.

        description : typing.Optional[str]
            Text describing what the tool does.

        fallback_content : typing.Optional[str]
            Text to use if the tool fails to generate content.

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        typing.Optional[ReturnUserDefinedTool]
            Success

        Examples
        --------
        from hume.client import AsyncHumeClient

        client = AsyncHumeClient(
            api_key="YOUR_API_KEY",
        )
        await client.empathic_voice.tools.create_tool_version(
            id="00183a3f-79ba-413d-9f3b-609864268bea",
            parameters='{ "type": "object", "properties": { "location": { "type": "string", "description": "The city and state, e.g. San Francisco, CA" }, "format": { "type": "string", "enum": ["celsius", "fahrenheit", "kelvin"], "description": "The temperature unit to use. Infer this from the users location." } }, "required": ["location", "format"] }',
            version_description="Fetches current weather and uses celsius, fahrenheit, or kelvin based on location of user.",
            fallback_content="Unable to fetch current weather.",
            description="This tool is for getting the current weather.",
        )
        """
        _response = await self._client_wrapper.httpx_client.request(
            f"v0/evi/tools/{jsonable_encoder(id)}",
            method="POST",
            json={
                "version_description": version_description,
                "description": description,
                "parameters": parameters,
                "fallback_content": fallback_content,
            },
            request_options=request_options,
            omit=OMIT,
        )
        if 200 <= _response.status_code < 300:
            return pydantic_v1.parse_obj_as(typing.Optional[ReturnUserDefinedTool], _response.json())  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    async def delete_tool(self, id: str, *, request_options: typing.Optional[RequestOptions] = None) -> None:
        """
        Parameters
        ----------
        id : str
            Identifier for a tool. Formatted as a UUID.

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        None

        Examples
        --------
        from hume.client import AsyncHumeClient

        client = AsyncHumeClient(
            api_key="YOUR_API_KEY",
        )
        await client.empathic_voice.tools.delete_tool(
            id="00183a3f-79ba-413d-9f3b-609864268bea",
        )
        """
        _response = await self._client_wrapper.httpx_client.request(
            f"v0/evi/tools/{jsonable_encoder(id)}", method="DELETE", request_options=request_options
        )
        if 200 <= _response.status_code < 300:
            return
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    async def update_tool_name(
        self, id: str, *, name: str, request_options: typing.Optional[RequestOptions] = None
    ) -> str:
        """
        Parameters
        ----------
        id : str
            Identifier for a tool. Formatted as a UUID.

        name : str
            Name applied to all versions of a particular Tool.

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        str
            Success

        Examples
        --------
        from hume.client import AsyncHumeClient

        client = AsyncHumeClient(
            api_key="YOUR_API_KEY",
        )
        await client.empathic_voice.tools.update_tool_name(
            id="00183a3f-79ba-413d-9f3b-609864268bea",
            name="get_current_temperature",
        )
        """
        _response = await self._client_wrapper.httpx_client.request(
            f"v0/evi/tools/{jsonable_encoder(id)}",
            method="PATCH",
            json={"name": name},
            request_options=request_options,
            omit=OMIT,
        )
        if 200 <= _response.status_code < 300:
            return _response.text  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    async def get_tool_version(
        self, id: str, version: int, *, request_options: typing.Optional[RequestOptions] = None
    ) -> typing.Optional[ReturnUserDefinedTool]:
        """
        Parameters
        ----------
        id : str
            Identifier for a tool. Formatted as a UUID.

        version : int
            Version number for a tool. Version numbers should be integers.

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        typing.Optional[ReturnUserDefinedTool]
            Success

        Examples
        --------
        from hume.client import AsyncHumeClient

        client = AsyncHumeClient(
            api_key="YOUR_API_KEY",
        )
        await client.empathic_voice.tools.get_tool_version(
            id="00183a3f-79ba-413d-9f3b-609864268bea",
            version=1,
        )
        """
        _response = await self._client_wrapper.httpx_client.request(
            f"v0/evi/tools/{jsonable_encoder(id)}/version/{jsonable_encoder(version)}",
            method="GET",
            request_options=request_options,
        )
        if 200 <= _response.status_code < 300:
            return pydantic_v1.parse_obj_as(typing.Optional[ReturnUserDefinedTool], _response.json())  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    async def delete_tool_version(
        self, id: str, version: int, *, request_options: typing.Optional[RequestOptions] = None
    ) -> None:
        """
        Parameters
        ----------
        id : str
            Identifier for a tool. Formatted as a UUID.

        version : int
            Version number for a tool. Version numbers should be integers.

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        None

        Examples
        --------
        from hume.client import AsyncHumeClient

        client = AsyncHumeClient(
            api_key="YOUR_API_KEY",
        )
        await client.empathic_voice.tools.delete_tool_version(
            id="00183a3f-79ba-413d-9f3b-609864268bea",
            version=1,
        )
        """
        _response = await self._client_wrapper.httpx_client.request(
            f"v0/evi/tools/{jsonable_encoder(id)}/version/{jsonable_encoder(version)}",
            method="DELETE",
            request_options=request_options,
        )
        if 200 <= _response.status_code < 300:
            return
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    async def update_tool_description(
        self,
        id: str,
        version: int,
        *,
        version_description: typing.Optional[str] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> typing.Optional[ReturnUserDefinedTool]:
        """
        Parameters
        ----------
        id : str
            Identifier for a tool. Formatted as a UUID.

        version : int
            Version number for a tool. Version numbers should be integers.

        version_description : typing.Optional[str]
            Description that is appended to a specific version of a Tool.

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        typing.Optional[ReturnUserDefinedTool]
            Success

        Examples
        --------
        from hume.client import AsyncHumeClient

        client = AsyncHumeClient(
            api_key="YOUR_API_KEY",
        )
        await client.empathic_voice.tools.update_tool_description(
            id="00183a3f-79ba-413d-9f3b-609864268bea",
            version=1,
            version_description="Fetches current temperature, precipitation, wind speed, AQI, and other weather conditions. Uses Celsius, Fahrenheit, or kelvin depending on user's region.",
        )
        """
        _response = await self._client_wrapper.httpx_client.request(
            f"v0/evi/tools/{jsonable_encoder(id)}/version/{jsonable_encoder(version)}",
            method="PATCH",
            json={"version_description": version_description},
            request_options=request_options,
            omit=OMIT,
        )
        if 200 <= _response.status_code < 300:
            return pydantic_v1.parse_obj_as(typing.Optional[ReturnUserDefinedTool], _response.json())  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)