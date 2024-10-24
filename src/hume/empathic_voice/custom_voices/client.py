# This file was auto-generated by Fern from our API Definition.

import typing
from ...core.client_wrapper import SyncClientWrapper
from ...core.request_options import RequestOptions
from ..types.return_paged_custom_voices import ReturnPagedCustomVoices
from ...core.pydantic_utilities import parse_obj_as
from ..errors.bad_request_error import BadRequestError
from ..types.error_response import ErrorResponse
from json.decoder import JSONDecodeError
from ...core.api_error import ApiError
from ..types.posted_custom_voice_base_voice import PostedCustomVoiceBaseVoice
from ..types.posted_custom_voice_parameters import PostedCustomVoiceParameters
from ..types.return_custom_voice import ReturnCustomVoice
from ...core.serialization import convert_and_respect_annotation_metadata
from ...core.jsonable_encoder import jsonable_encoder
from ...core.client_wrapper import AsyncClientWrapper

# this is used as the default value for optional parameters
OMIT = typing.cast(typing.Any, ...)


class CustomVoicesClient:
    def __init__(self, *, client_wrapper: SyncClientWrapper):
        self._client_wrapper = client_wrapper

    def list_custom_voices(
        self,
        *,
        page_number: typing.Optional[int] = None,
        page_size: typing.Optional[int] = None,
        name: typing.Optional[str] = None,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> ReturnPagedCustomVoices:
        """
        Fetches a paginated list of **Custom Voices**.

        Refer to our [voices guide](/docs/empathic-voice-interface-evi/voices) for details on creating a custom voice.

        Parameters
        ----------
        page_number : typing.Optional[int]
            Specifies the page number to retrieve, enabling pagination.

            This parameter uses zero-based indexing. For example, setting `page_number` to 0 retrieves the first page of results (items 0-9 if `page_size` is 10), setting `page_number` to 1 retrieves the second page (items 10-19), and so on. Defaults to 0, which retrieves the first page.

        page_size : typing.Optional[int]
            Specifies the maximum number of results to include per page, enabling pagination. The value must be between 1 and 100, inclusive.

            For example, if `page_size` is set to 10, each page will include up to 10 items. Defaults to 10.

        name : typing.Optional[str]
            Filter to only include custom voices with this name.

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        ReturnPagedCustomVoices
            Success

        Examples
        --------
        from hume import HumeClient

        client = HumeClient(
            api_key="YOUR_API_KEY",
        )
        client.empathic_voice.custom_voices.list_custom_voices()
        """
        _response = self._client_wrapper.httpx_client.request(
            "v0/evi/custom_voices",
            method="GET",
            params={
                "page_number": page_number,
                "page_size": page_size,
                "name": name,
            },
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(
                    ReturnPagedCustomVoices,
                    parse_obj_as(
                        type_=ReturnPagedCustomVoices,  # type: ignore
                        object_=_response.json(),
                    ),
                )
            if _response.status_code == 400:
                raise BadRequestError(
                    typing.cast(
                        ErrorResponse,
                        parse_obj_as(
                            type_=ErrorResponse,  # type: ignore
                            object_=_response.json(),
                        ),
                    )
                )
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def create_custom_voice(
        self,
        *,
        name: str,
        base_voice: PostedCustomVoiceBaseVoice,
        parameters: typing.Optional[PostedCustomVoiceParameters] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> ReturnCustomVoice:
        """
        Creates a **Custom Voice** that can be added to an [EVI configuration](/reference/empathic-voice-interface-evi/configs/create-config).

        Refer to our [voices guide](/docs/empathic-voice-interface-evi/voices) for details on creating a custom voice.

        Parameters
        ----------
        name : str
            The name of the Custom Voice. Maximum length of 75 characters. Will be converted to all-uppercase. (e.g., "sample voice" becomes "SAMPLE VOICE")

        base_voice : PostedCustomVoiceBaseVoice
            Specifies the base voice used to create the Custom Voice.

        parameters : typing.Optional[PostedCustomVoiceParameters]
            The specified attributes of a Custom Voice.

            If no parameters are specified then all attributes will be set to their defaults, meaning no modfications will be made to the base voice.

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        ReturnCustomVoice
            Created

        Examples
        --------
        from hume import HumeClient

        client = HumeClient(
            api_key="YOUR_API_KEY",
        )
        client.empathic_voice.custom_voices.create_custom_voice(
            name="name",
            base_voice="ITO",
        )
        """
        _response = self._client_wrapper.httpx_client.request(
            "v0/evi/custom_voices",
            method="POST",
            json={
                "name": name,
                "base_voice": base_voice,
                "parameters": convert_and_respect_annotation_metadata(
                    object_=parameters, annotation=PostedCustomVoiceParameters, direction="write"
                ),
                "parameter_model": "20241004-11parameter",
            },
            request_options=request_options,
            omit=OMIT,
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(
                    ReturnCustomVoice,
                    parse_obj_as(
                        type_=ReturnCustomVoice,  # type: ignore
                        object_=_response.json(),
                    ),
                )
            if _response.status_code == 400:
                raise BadRequestError(
                    typing.cast(
                        ErrorResponse,
                        parse_obj_as(
                            type_=ErrorResponse,  # type: ignore
                            object_=_response.json(),
                        ),
                    )
                )
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def get_custom_voice(
        self, id: str, *, request_options: typing.Optional[RequestOptions] = None
    ) -> ReturnCustomVoice:
        """
        Fetches a specific **Custom Voice** by ID.

        Refer to our [voices guide](/docs/empathic-voice-interface-evi/voices) for details on creating a custom voice.

        Parameters
        ----------
        id : str
            Identifier for a Custom Voice. Formatted as a UUID.

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        ReturnCustomVoice
            Success

        Examples
        --------
        from hume import HumeClient

        client = HumeClient(
            api_key="YOUR_API_KEY",
        )
        client.empathic_voice.custom_voices.get_custom_voice(
            id="id",
        )
        """
        _response = self._client_wrapper.httpx_client.request(
            f"v0/evi/custom_voices/{jsonable_encoder(id)}",
            method="GET",
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(
                    ReturnCustomVoice,
                    parse_obj_as(
                        type_=ReturnCustomVoice,  # type: ignore
                        object_=_response.json(),
                    ),
                )
            if _response.status_code == 400:
                raise BadRequestError(
                    typing.cast(
                        ErrorResponse,
                        parse_obj_as(
                            type_=ErrorResponse,  # type: ignore
                            object_=_response.json(),
                        ),
                    )
                )
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def create_custom_voice_version(
        self,
        id: str,
        *,
        name: str,
        base_voice: PostedCustomVoiceBaseVoice,
        parameters: typing.Optional[PostedCustomVoiceParameters] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> ReturnCustomVoice:
        """
        Updates a **Custom Voice** by creating a new version of the **Custom Voice**.

        Refer to our [voices guide](/docs/empathic-voice-interface-evi/voices) for details on creating a custom voice.

        Parameters
        ----------
        id : str
            Identifier for a Custom Voice. Formatted as a UUID.

        name : str
            The name of the Custom Voice. Maximum length of 75 characters. Will be converted to all-uppercase. (e.g., "sample voice" becomes "SAMPLE VOICE")

        base_voice : PostedCustomVoiceBaseVoice
            Specifies the base voice used to create the Custom Voice.

        parameters : typing.Optional[PostedCustomVoiceParameters]
            The specified attributes of a Custom Voice.

            If no parameters are specified then all attributes will be set to their defaults, meaning no modfications will be made to the base voice.

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        ReturnCustomVoice
            Created

        Examples
        --------
        from hume import HumeClient

        client = HumeClient(
            api_key="YOUR_API_KEY",
        )
        client.empathic_voice.custom_voices.create_custom_voice_version(
            id="id",
            name="name",
            base_voice="ITO",
        )
        """
        _response = self._client_wrapper.httpx_client.request(
            f"v0/evi/custom_voices/{jsonable_encoder(id)}",
            method="POST",
            json={
                "name": name,
                "base_voice": base_voice,
                "parameters": convert_and_respect_annotation_metadata(
                    object_=parameters, annotation=PostedCustomVoiceParameters, direction="write"
                ),
                "parameter_model": "20241004-11parameter",
            },
            request_options=request_options,
            omit=OMIT,
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(
                    ReturnCustomVoice,
                    parse_obj_as(
                        type_=ReturnCustomVoice,  # type: ignore
                        object_=_response.json(),
                    ),
                )
            if _response.status_code == 400:
                raise BadRequestError(
                    typing.cast(
                        ErrorResponse,
                        parse_obj_as(
                            type_=ErrorResponse,  # type: ignore
                            object_=_response.json(),
                        ),
                    )
                )
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def delete_custom_voice(self, id: str, *, request_options: typing.Optional[RequestOptions] = None) -> None:
        """
        Deletes a **Custom Voice** and its versions.

        Refer to our [voices guide](/docs/empathic-voice-interface-evi/voices) for details on creating a custom voice.

        Parameters
        ----------
        id : str
            Identifier for a Custom Voice. Formatted as a UUID.

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        None

        Examples
        --------
        from hume import HumeClient

        client = HumeClient(
            api_key="YOUR_API_KEY",
        )
        client.empathic_voice.custom_voices.delete_custom_voice(
            id="id",
        )
        """
        _response = self._client_wrapper.httpx_client.request(
            f"v0/evi/custom_voices/{jsonable_encoder(id)}",
            method="DELETE",
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                return
            if _response.status_code == 400:
                raise BadRequestError(
                    typing.cast(
                        ErrorResponse,
                        parse_obj_as(
                            type_=ErrorResponse,  # type: ignore
                            object_=_response.json(),
                        ),
                    )
                )
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def update_custom_voice_name(
        self, id: str, *, name: str, request_options: typing.Optional[RequestOptions] = None
    ) -> str:
        """
        Updates the name of a **Custom Voice**.

        Refer to our [voices guide](/docs/empathic-voice-interface-evi/voices) for details on creating a custom voice.

        Parameters
        ----------
        id : str
            Identifier for a Custom Voice. Formatted as a UUID.

        name : str
            The name of the Custom Voice. Maximum length of 75 characters. Will be converted to all-uppercase. (e.g., "sample voice" becomes "SAMPLE VOICE")

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        str
            Success

        Examples
        --------
        from hume import HumeClient

        client = HumeClient(
            api_key="YOUR_API_KEY",
        )
        client.empathic_voice.custom_voices.update_custom_voice_name(
            id="string",
            name="string",
        )
        """
        _response = self._client_wrapper.httpx_client.request(
            f"v0/evi/custom_voices/{jsonable_encoder(id)}",
            method="PATCH",
            json={
                "name": name,
            },
            request_options=request_options,
            omit=OMIT,
        )
        try:
            if 200 <= _response.status_code < 300:
                return _response.text  # type: ignore
            if _response.status_code == 400:
                raise BadRequestError(
                    typing.cast(
                        ErrorResponse,
                        parse_obj_as(
                            type_=ErrorResponse,  # type: ignore
                            object_=_response.json(),
                        ),
                    )
                )
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)


class AsyncCustomVoicesClient:
    def __init__(self, *, client_wrapper: AsyncClientWrapper):
        self._client_wrapper = client_wrapper

    async def list_custom_voices(
        self,
        *,
        page_number: typing.Optional[int] = None,
        page_size: typing.Optional[int] = None,
        name: typing.Optional[str] = None,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> ReturnPagedCustomVoices:
        """
        Fetches a paginated list of **Custom Voices**.

        Refer to our [voices guide](/docs/empathic-voice-interface-evi/voices) for details on creating a custom voice.

        Parameters
        ----------
        page_number : typing.Optional[int]
            Specifies the page number to retrieve, enabling pagination.

            This parameter uses zero-based indexing. For example, setting `page_number` to 0 retrieves the first page of results (items 0-9 if `page_size` is 10), setting `page_number` to 1 retrieves the second page (items 10-19), and so on. Defaults to 0, which retrieves the first page.

        page_size : typing.Optional[int]
            Specifies the maximum number of results to include per page, enabling pagination. The value must be between 1 and 100, inclusive.

            For example, if `page_size` is set to 10, each page will include up to 10 items. Defaults to 10.

        name : typing.Optional[str]
            Filter to only include custom voices with this name.

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        ReturnPagedCustomVoices
            Success

        Examples
        --------
        import asyncio

        from hume import AsyncHumeClient

        client = AsyncHumeClient(
            api_key="YOUR_API_KEY",
        )


        async def main() -> None:
            await client.empathic_voice.custom_voices.list_custom_voices()


        asyncio.run(main())
        """
        _response = await self._client_wrapper.httpx_client.request(
            "v0/evi/custom_voices",
            method="GET",
            params={
                "page_number": page_number,
                "page_size": page_size,
                "name": name,
            },
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(
                    ReturnPagedCustomVoices,
                    parse_obj_as(
                        type_=ReturnPagedCustomVoices,  # type: ignore
                        object_=_response.json(),
                    ),
                )
            if _response.status_code == 400:
                raise BadRequestError(
                    typing.cast(
                        ErrorResponse,
                        parse_obj_as(
                            type_=ErrorResponse,  # type: ignore
                            object_=_response.json(),
                        ),
                    )
                )
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    async def create_custom_voice(
        self,
        *,
        name: str,
        base_voice: PostedCustomVoiceBaseVoice,
        parameters: typing.Optional[PostedCustomVoiceParameters] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> ReturnCustomVoice:
        """
        Creates a **Custom Voice** that can be added to an [EVI configuration](/reference/empathic-voice-interface-evi/configs/create-config).

        Refer to our [voices guide](/docs/empathic-voice-interface-evi/voices) for details on creating a custom voice.

        Parameters
        ----------
        name : str
            The name of the Custom Voice. Maximum length of 75 characters. Will be converted to all-uppercase. (e.g., "sample voice" becomes "SAMPLE VOICE")

        base_voice : PostedCustomVoiceBaseVoice
            Specifies the base voice used to create the Custom Voice.

        parameters : typing.Optional[PostedCustomVoiceParameters]
            The specified attributes of a Custom Voice.

            If no parameters are specified then all attributes will be set to their defaults, meaning no modfications will be made to the base voice.

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        ReturnCustomVoice
            Created

        Examples
        --------
        import asyncio

        from hume import AsyncHumeClient

        client = AsyncHumeClient(
            api_key="YOUR_API_KEY",
        )


        async def main() -> None:
            await client.empathic_voice.custom_voices.create_custom_voice(
                name="name",
                base_voice="ITO",
            )


        asyncio.run(main())
        """
        _response = await self._client_wrapper.httpx_client.request(
            "v0/evi/custom_voices",
            method="POST",
            json={
                "name": name,
                "base_voice": base_voice,
                "parameters": convert_and_respect_annotation_metadata(
                    object_=parameters, annotation=PostedCustomVoiceParameters, direction="write"
                ),
                "parameter_model": "20241004-11parameter",
            },
            request_options=request_options,
            omit=OMIT,
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(
                    ReturnCustomVoice,
                    parse_obj_as(
                        type_=ReturnCustomVoice,  # type: ignore
                        object_=_response.json(),
                    ),
                )
            if _response.status_code == 400:
                raise BadRequestError(
                    typing.cast(
                        ErrorResponse,
                        parse_obj_as(
                            type_=ErrorResponse,  # type: ignore
                            object_=_response.json(),
                        ),
                    )
                )
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    async def get_custom_voice(
        self, id: str, *, request_options: typing.Optional[RequestOptions] = None
    ) -> ReturnCustomVoice:
        """
        Fetches a specific **Custom Voice** by ID.

        Refer to our [voices guide](/docs/empathic-voice-interface-evi/voices) for details on creating a custom voice.

        Parameters
        ----------
        id : str
            Identifier for a Custom Voice. Formatted as a UUID.

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        ReturnCustomVoice
            Success

        Examples
        --------
        import asyncio

        from hume import AsyncHumeClient

        client = AsyncHumeClient(
            api_key="YOUR_API_KEY",
        )


        async def main() -> None:
            await client.empathic_voice.custom_voices.get_custom_voice(
                id="id",
            )


        asyncio.run(main())
        """
        _response = await self._client_wrapper.httpx_client.request(
            f"v0/evi/custom_voices/{jsonable_encoder(id)}",
            method="GET",
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(
                    ReturnCustomVoice,
                    parse_obj_as(
                        type_=ReturnCustomVoice,  # type: ignore
                        object_=_response.json(),
                    ),
                )
            if _response.status_code == 400:
                raise BadRequestError(
                    typing.cast(
                        ErrorResponse,
                        parse_obj_as(
                            type_=ErrorResponse,  # type: ignore
                            object_=_response.json(),
                        ),
                    )
                )
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    async def create_custom_voice_version(
        self,
        id: str,
        *,
        name: str,
        base_voice: PostedCustomVoiceBaseVoice,
        parameters: typing.Optional[PostedCustomVoiceParameters] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> ReturnCustomVoice:
        """
        Updates a **Custom Voice** by creating a new version of the **Custom Voice**.

        Refer to our [voices guide](/docs/empathic-voice-interface-evi/voices) for details on creating a custom voice.

        Parameters
        ----------
        id : str
            Identifier for a Custom Voice. Formatted as a UUID.

        name : str
            The name of the Custom Voice. Maximum length of 75 characters. Will be converted to all-uppercase. (e.g., "sample voice" becomes "SAMPLE VOICE")

        base_voice : PostedCustomVoiceBaseVoice
            Specifies the base voice used to create the Custom Voice.

        parameters : typing.Optional[PostedCustomVoiceParameters]
            The specified attributes of a Custom Voice.

            If no parameters are specified then all attributes will be set to their defaults, meaning no modfications will be made to the base voice.

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        ReturnCustomVoice
            Created

        Examples
        --------
        import asyncio

        from hume import AsyncHumeClient

        client = AsyncHumeClient(
            api_key="YOUR_API_KEY",
        )


        async def main() -> None:
            await client.empathic_voice.custom_voices.create_custom_voice_version(
                id="id",
                name="name",
                base_voice="ITO",
            )


        asyncio.run(main())
        """
        _response = await self._client_wrapper.httpx_client.request(
            f"v0/evi/custom_voices/{jsonable_encoder(id)}",
            method="POST",
            json={
                "name": name,
                "base_voice": base_voice,
                "parameters": convert_and_respect_annotation_metadata(
                    object_=parameters, annotation=PostedCustomVoiceParameters, direction="write"
                ),
                "parameter_model": "20241004-11parameter",
            },
            request_options=request_options,
            omit=OMIT,
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(
                    ReturnCustomVoice,
                    parse_obj_as(
                        type_=ReturnCustomVoice,  # type: ignore
                        object_=_response.json(),
                    ),
                )
            if _response.status_code == 400:
                raise BadRequestError(
                    typing.cast(
                        ErrorResponse,
                        parse_obj_as(
                            type_=ErrorResponse,  # type: ignore
                            object_=_response.json(),
                        ),
                    )
                )
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    async def delete_custom_voice(self, id: str, *, request_options: typing.Optional[RequestOptions] = None) -> None:
        """
        Deletes a **Custom Voice** and its versions.

        Refer to our [voices guide](/docs/empathic-voice-interface-evi/voices) for details on creating a custom voice.

        Parameters
        ----------
        id : str
            Identifier for a Custom Voice. Formatted as a UUID.

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        None

        Examples
        --------
        import asyncio

        from hume import AsyncHumeClient

        client = AsyncHumeClient(
            api_key="YOUR_API_KEY",
        )


        async def main() -> None:
            await client.empathic_voice.custom_voices.delete_custom_voice(
                id="id",
            )


        asyncio.run(main())
        """
        _response = await self._client_wrapper.httpx_client.request(
            f"v0/evi/custom_voices/{jsonable_encoder(id)}",
            method="DELETE",
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                return
            if _response.status_code == 400:
                raise BadRequestError(
                    typing.cast(
                        ErrorResponse,
                        parse_obj_as(
                            type_=ErrorResponse,  # type: ignore
                            object_=_response.json(),
                        ),
                    )
                )
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    async def update_custom_voice_name(
        self, id: str, *, name: str, request_options: typing.Optional[RequestOptions] = None
    ) -> str:
        """
        Updates the name of a **Custom Voice**.

        Refer to our [voices guide](/docs/empathic-voice-interface-evi/voices) for details on creating a custom voice.

        Parameters
        ----------
        id : str
            Identifier for a Custom Voice. Formatted as a UUID.

        name : str
            The name of the Custom Voice. Maximum length of 75 characters. Will be converted to all-uppercase. (e.g., "sample voice" becomes "SAMPLE VOICE")

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        str
            Success

        Examples
        --------
        import asyncio

        from hume import AsyncHumeClient

        client = AsyncHumeClient(
            api_key="YOUR_API_KEY",
        )


        async def main() -> None:
            await client.empathic_voice.custom_voices.update_custom_voice_name(
                id="string",
                name="string",
            )


        asyncio.run(main())
        """
        _response = await self._client_wrapper.httpx_client.request(
            f"v0/evi/custom_voices/{jsonable_encoder(id)}",
            method="PATCH",
            json={
                "name": name,
            },
            request_options=request_options,
            omit=OMIT,
        )
        try:
            if 200 <= _response.status_code < 300:
                return _response.text  # type: ignore
            if _response.status_code == 400:
                raise BadRequestError(
                    typing.cast(
                        ErrorResponse,
                        parse_obj_as(
                            type_=ErrorResponse,  # type: ignore
                            object_=_response.json(),
                        ),
                    )
                )
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)
