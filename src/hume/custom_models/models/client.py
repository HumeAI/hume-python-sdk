# This file was auto-generated by Fern from our API Definition.

import typing
from json.decoder import JSONDecodeError

from ...core.api_error import ApiError
from ...core.client_wrapper import AsyncClientWrapper, SyncClientWrapper
from ...core.jsonable_encoder import jsonable_encoder
from ...core.pagination import AsyncPager, SyncPager
from ...core.pydantic_utilities import pydantic_v1
from ...core.request_options import RequestOptions
from ..types.external_model import ExternalModel
from ..types.external_model_version import ExternalModelVersion
from ..types.model_page import ModelPage

# this is used as the default value for optional parameters
OMIT = typing.cast(typing.Any, ...)


class ModelsClient:
    def __init__(self, *, client_wrapper: SyncClientWrapper):
        self._client_wrapper = client_wrapper

    def list_models(
        self,
        *,
        name: typing.Optional[str] = None,
        page_number: typing.Optional[int] = None,
        page_size: typing.Optional[int] = None,
        shared_assets: typing.Optional[bool] = None,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> SyncPager[ExternalModel]:
        """
        Returns 200 if successful

        Parameters
        ----------
        name : typing.Optional[str]
            Model name to be queried

        page_number : typing.Optional[int]
            Index of the first result

        page_size : typing.Optional[int]
            Maximum number of results

        shared_assets : typing.Optional[bool]
            `True` Will show all assets owned by you and shared with you. `False` Will show only your assets. Default: `False`

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        SyncPager[ExternalModel]
            Success

        Examples
        --------
        from hume.client import HumeClient

        client = HumeClient(
            api_key="YOUR_API_KEY",
        )
        client.custom_models.models.list_models()
        """
        page_number = page_number or 1
        _response = self._client_wrapper.httpx_client.request(
            "v0/registry/models",
            method="GET",
            params={"name": name, "page_number": page_number, "page_size": page_size, "shared_assets": shared_assets},
            request_options=request_options,
        )
        if 200 <= _response.status_code < 300:
            _parsed_response = pydantic_v1.parse_obj_as(ModelPage, _response.json())  # type: ignore
            _has_next = True
            _get_next = lambda: self.list_models(
                name=name,
                page_number=page_number + 1,
                page_size=page_size,
                shared_assets=shared_assets,
                request_options=request_options,
            )
            _items = _parsed_response.content
            return SyncPager(has_next=_has_next, items=_items, get_next=_get_next)
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def get_model_details(self, id: str, *, request_options: typing.Optional[RequestOptions] = None) -> ExternalModel:
        """
        Returns 200 if successful

        Parameters
        ----------
        id : str
            Hume-generated ID of a Model

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        ExternalModel
            Success

        Examples
        --------
        from hume.client import HumeClient

        client = HumeClient(
            api_key="YOUR_API_KEY",
        )
        client.custom_models.models.get_model_details(
            id="id",
        )
        """
        _response = self._client_wrapper.httpx_client.request(
            f"v0/registry/models/{jsonable_encoder(id)}", method="GET", request_options=request_options
        )
        if 200 <= _response.status_code < 300:
            return pydantic_v1.parse_obj_as(ExternalModel, _response.json())  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def update_model_name(
        self, id: str, *, name: str, request_options: typing.Optional[RequestOptions] = None
    ) -> ExternalModel:
        """
        Returns 200 if successful

        Parameters
        ----------
        id : str
            Hume-generated ID of a Model

        name : str
            New Model name

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        ExternalModel
            Success

        Examples
        --------
        from hume.client import HumeClient

        client = HumeClient(
            api_key="YOUR_API_KEY",
        )
        client.custom_models.models.update_model_name(
            id="id",
            name="name",
        )
        """
        _response = self._client_wrapper.httpx_client.request(
            f"v0/registry/models/{jsonable_encoder(id)}",
            method="PATCH",
            params={"name": name},
            request_options=request_options,
        )
        if 200 <= _response.status_code < 300:
            return pydantic_v1.parse_obj_as(ExternalModel, _response.json())  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def list_model_versions(
        self,
        *,
        id: typing.Optional[typing.Union[str, typing.Sequence[str]]] = None,
        name: typing.Optional[str] = None,
        version: typing.Optional[str] = None,
        shared_assets: typing.Optional[bool] = None,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> typing.List[ExternalModelVersion]:
        """
        Returns 200 if successful

        Parameters
        ----------
        id : typing.Optional[typing.Union[str, typing.Sequence[str]]]
            Hume-generated Model Version IDs to be queried

        name : typing.Optional[str]
            Model version name to be queried

        version : typing.Optional[str]
            Model version number to be queried

        shared_assets : typing.Optional[bool]
            `True` Will show all assets owned by you and shared with you. `False` Will show only your assets. Default: `False`

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        typing.List[ExternalModelVersion]
            Success

        Examples
        --------
        from hume.client import HumeClient

        client = HumeClient(
            api_key="YOUR_API_KEY",
        )
        client.custom_models.models.list_model_versions()
        """
        _response = self._client_wrapper.httpx_client.request(
            "v0/registry/models/version",
            method="GET",
            params={"id": id, "name": name, "version": version, "shared_assets": shared_assets},
            request_options=request_options,
        )
        if 200 <= _response.status_code < 300:
            return pydantic_v1.parse_obj_as(typing.List[ExternalModelVersion], _response.json())  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def get_model_version(
        self,
        id: str,
        *,
        shared_assets: typing.Optional[bool] = None,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> ExternalModelVersion:
        """
        Returns 200 if successful

        Parameters
        ----------
        id : str
            Hume-generated ID of a Model version

        shared_assets : typing.Optional[bool]
            `True` Will show all assets owned by you and shared with you. `False` Will show only your assets. Default: `False`

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        ExternalModelVersion
            Success

        Examples
        --------
        from hume.client import HumeClient

        client = HumeClient(
            api_key="YOUR_API_KEY",
        )
        client.custom_models.models.get_model_version(
            id="id",
        )
        """
        _response = self._client_wrapper.httpx_client.request(
            f"v0/registry/models/version/{jsonable_encoder(id)}",
            method="GET",
            params={"shared_assets": shared_assets},
            request_options=request_options,
        )
        if 200 <= _response.status_code < 300:
            return pydantic_v1.parse_obj_as(ExternalModelVersion, _response.json())  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def update_model_description(
        self, id: str, *, request: str, request_options: typing.Optional[RequestOptions] = None
    ) -> ExternalModelVersion:
        """
        Returns 200 if successful

        Parameters
        ----------
        id : str
            Hume-generated ID of a Model Version

        request : str

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        ExternalModelVersion
            Success

        Examples
        --------
        from hume.client import HumeClient

        client = HumeClient(
            api_key="YOUR_API_KEY",
        )
        client.custom_models.models.update_model_description(
            id="id",
            request="string",
        )
        """
        _response = self._client_wrapper.httpx_client.request(
            f"v0/registry/models/version/{jsonable_encoder(id)}",
            method="PATCH",
            json=request,
            request_options=request_options,
            omit=OMIT,
        )
        if 200 <= _response.status_code < 300:
            return pydantic_v1.parse_obj_as(ExternalModelVersion, _response.json())  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)


class AsyncModelsClient:
    def __init__(self, *, client_wrapper: AsyncClientWrapper):
        self._client_wrapper = client_wrapper

    async def list_models(
        self,
        *,
        name: typing.Optional[str] = None,
        page_number: typing.Optional[int] = None,
        page_size: typing.Optional[int] = None,
        shared_assets: typing.Optional[bool] = None,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> AsyncPager[ExternalModel]:
        """
        Returns 200 if successful

        Parameters
        ----------
        name : typing.Optional[str]
            Model name to be queried

        page_number : typing.Optional[int]
            Index of the first result

        page_size : typing.Optional[int]
            Maximum number of results

        shared_assets : typing.Optional[bool]
            `True` Will show all assets owned by you and shared with you. `False` Will show only your assets. Default: `False`

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        AsyncPager[ExternalModel]
            Success

        Examples
        --------
        from hume.client import AsyncHumeClient

        client = AsyncHumeClient(
            api_key="YOUR_API_KEY",
        )
        await client.custom_models.models.list_models()
        """
        page_number = page_number or 1
        _response = await self._client_wrapper.httpx_client.request(
            "v0/registry/models",
            method="GET",
            params={"name": name, "page_number": page_number, "page_size": page_size, "shared_assets": shared_assets},
            request_options=request_options,
        )
        if 200 <= _response.status_code < 300:
            _parsed_response = pydantic_v1.parse_obj_as(ModelPage, _response.json())  # type: ignore
            _has_next = True
            _get_next = lambda: self.list_models(
                name=name,
                page_number=page_number + 1,
                page_size=page_size,
                shared_assets=shared_assets,
                request_options=request_options,
            )
            _items = _parsed_response.content
            return AsyncPager(has_next=_has_next, items=_items, get_next=_get_next)
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    async def get_model_details(
        self, id: str, *, request_options: typing.Optional[RequestOptions] = None
    ) -> ExternalModel:
        """
        Returns 200 if successful

        Parameters
        ----------
        id : str
            Hume-generated ID of a Model

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        ExternalModel
            Success

        Examples
        --------
        from hume.client import AsyncHumeClient

        client = AsyncHumeClient(
            api_key="YOUR_API_KEY",
        )
        await client.custom_models.models.get_model_details(
            id="id",
        )
        """
        _response = await self._client_wrapper.httpx_client.request(
            f"v0/registry/models/{jsonable_encoder(id)}", method="GET", request_options=request_options
        )
        if 200 <= _response.status_code < 300:
            return pydantic_v1.parse_obj_as(ExternalModel, _response.json())  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    async def update_model_name(
        self, id: str, *, name: str, request_options: typing.Optional[RequestOptions] = None
    ) -> ExternalModel:
        """
        Returns 200 if successful

        Parameters
        ----------
        id : str
            Hume-generated ID of a Model

        name : str
            New Model name

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        ExternalModel
            Success

        Examples
        --------
        from hume.client import AsyncHumeClient

        client = AsyncHumeClient(
            api_key="YOUR_API_KEY",
        )
        await client.custom_models.models.update_model_name(
            id="id",
            name="name",
        )
        """
        _response = await self._client_wrapper.httpx_client.request(
            f"v0/registry/models/{jsonable_encoder(id)}",
            method="PATCH",
            params={"name": name},
            request_options=request_options,
        )
        if 200 <= _response.status_code < 300:
            return pydantic_v1.parse_obj_as(ExternalModel, _response.json())  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    async def list_model_versions(
        self,
        *,
        id: typing.Optional[typing.Union[str, typing.Sequence[str]]] = None,
        name: typing.Optional[str] = None,
        version: typing.Optional[str] = None,
        shared_assets: typing.Optional[bool] = None,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> typing.List[ExternalModelVersion]:
        """
        Returns 200 if successful

        Parameters
        ----------
        id : typing.Optional[typing.Union[str, typing.Sequence[str]]]
            Hume-generated Model Version IDs to be queried

        name : typing.Optional[str]
            Model version name to be queried

        version : typing.Optional[str]
            Model version number to be queried

        shared_assets : typing.Optional[bool]
            `True` Will show all assets owned by you and shared with you. `False` Will show only your assets. Default: `False`

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        typing.List[ExternalModelVersion]
            Success

        Examples
        --------
        from hume.client import AsyncHumeClient

        client = AsyncHumeClient(
            api_key="YOUR_API_KEY",
        )
        await client.custom_models.models.list_model_versions()
        """
        _response = await self._client_wrapper.httpx_client.request(
            "v0/registry/models/version",
            method="GET",
            params={"id": id, "name": name, "version": version, "shared_assets": shared_assets},
            request_options=request_options,
        )
        if 200 <= _response.status_code < 300:
            return pydantic_v1.parse_obj_as(typing.List[ExternalModelVersion], _response.json())  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    async def get_model_version(
        self,
        id: str,
        *,
        shared_assets: typing.Optional[bool] = None,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> ExternalModelVersion:
        """
        Returns 200 if successful

        Parameters
        ----------
        id : str
            Hume-generated ID of a Model version

        shared_assets : typing.Optional[bool]
            `True` Will show all assets owned by you and shared with you. `False` Will show only your assets. Default: `False`

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        ExternalModelVersion
            Success

        Examples
        --------
        from hume.client import AsyncHumeClient

        client = AsyncHumeClient(
            api_key="YOUR_API_KEY",
        )
        await client.custom_models.models.get_model_version(
            id="id",
        )
        """
        _response = await self._client_wrapper.httpx_client.request(
            f"v0/registry/models/version/{jsonable_encoder(id)}",
            method="GET",
            params={"shared_assets": shared_assets},
            request_options=request_options,
        )
        if 200 <= _response.status_code < 300:
            return pydantic_v1.parse_obj_as(ExternalModelVersion, _response.json())  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    async def update_model_description(
        self, id: str, *, request: str, request_options: typing.Optional[RequestOptions] = None
    ) -> ExternalModelVersion:
        """
        Returns 200 if successful

        Parameters
        ----------
        id : str
            Hume-generated ID of a Model Version

        request : str

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        ExternalModelVersion
            Success

        Examples
        --------
        from hume.client import AsyncHumeClient

        client = AsyncHumeClient(
            api_key="YOUR_API_KEY",
        )
        await client.custom_models.models.update_model_description(
            id="id",
            request="string",
        )
        """
        _response = await self._client_wrapper.httpx_client.request(
            f"v0/registry/models/version/{jsonable_encoder(id)}",
            method="PATCH",
            json=request,
            request_options=request_options,
            omit=OMIT,
        )
        if 200 <= _response.status_code < 300:
            return pydantic_v1.parse_obj_as(ExternalModelVersion, _response.json())  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)
