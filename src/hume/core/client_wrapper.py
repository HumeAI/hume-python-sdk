# THIS FILE IS MANUALLY MAINTAINED: see .fernignore

import typing

import httpx

from .http_client import AsyncHttpClient, HttpClient
from importlib.metadata import version


class BaseClientWrapper:
    def __init__(self, *, api_key: typing.Optional[str] = None, base_url: str, timeout: typing.Optional[float] = None):
        self.api_key = api_key
        self._base_url = base_url
        self._timeout = timeout

    def get_headers(self, include_auth: bool = True) -> typing.Dict[str, str]:
        headers: typing.Dict[str, str] = {
            "X-Fern-Language": "Python",
            "X-Fern-SDK-Name": "hume",
            "X-Fern-SDK-Version": version("hume"),
        }
        if self.api_key is not None and include_auth:
            headers["X-Hume-Api-Key"] = self.api_key
        return headers

    def get_base_url(self) -> str:
        return self._base_url

    def get_timeout(self) -> typing.Optional[float]:
        return self._timeout


class SyncClientWrapper(BaseClientWrapper):
    def __init__(
        self,
        *,
        api_key: typing.Optional[str] = None,
        base_url: str,
        timeout: typing.Optional[float] = None,
        httpx_client: httpx.Client
    ):
        super().__init__(api_key=api_key, base_url=base_url, timeout=timeout)
        self.httpx_client = HttpClient(
            httpx_client=httpx_client,
            base_headers=lambda: self.get_headers(),
            base_timeout=lambda: self.get_timeout(),
            base_url=lambda: self.get_base_url(),
        )


class AsyncClientWrapper(BaseClientWrapper):
    def __init__(
        self,
        *,
        api_key: typing.Optional[str] = None,
        base_url: str,
        timeout: typing.Optional[float] = None,
        httpx_client: httpx.AsyncClient
    ):
        super().__init__(api_key=api_key, base_url=base_url, timeout=timeout)
        self.httpx_client = AsyncHttpClient(
            httpx_client=httpx_client,
            base_headers=lambda: self.get_headers(),
            base_timeout=lambda: self.get_timeout(),
            base_url=lambda: self.get_base_url(),
        )
