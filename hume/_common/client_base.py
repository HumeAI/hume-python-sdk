"""Base class for Hume clients."""

import logging
from importlib.metadata import version
from typing import ClassVar, Dict, Optional

from httpx import Client as HttpClient
from httpx import HTTPTransport, Response

from hume._common.protocol import Protocol
from hume._common.utilities.paging_utilities import Paging
from hume.error.hume_client_exception import HumeClientException

logger = logging.getLogger(__name__)


# pylint: disable=too-many-instance-attributes
class ClientBase:
    """Base class for Hume API clients."""

    DEFAULT_PAGE_SIZE: ClassVar[int] = 50
    DEFAULT_RETRY_BACKOFF_FACTOR: ClassVar[int] = 2
    DEFAULT_RETRY_TIMEOUT: ClassVar[int] = 30 * 60
    DEFAULT_HTTP_RETRIES: ClassVar[int] = 3
    DEFAULT_HTTP_TIMEOUT: ClassVar[int] = 30
    DEFAULT_WS_OPEN_TIMEOUT: ClassVar[int] = 10
    DEFAULT_WS_CLOSE_TIMEOUT: ClassVar[int] = 10

    DEFAULT_API_VERSION: ClassVar[str] = "v0"
    DEFAULT_API_HTTP_BASE_URL: ClassVar[str] = "https://api.hume.ai"
    DEFAULT_API_WS_BASE_URI: ClassVar[str] = "wss://api.hume.ai"

    PAGING_LIMIT: ClassVar[int] = 100_000

    def __init__(
        self,
        api_key: str,
        *,
        page_size: int = DEFAULT_PAGE_SIZE,
        retry_backoff_factor: float = DEFAULT_RETRY_BACKOFF_FACTOR,
        retry_timeout: float = DEFAULT_RETRY_TIMEOUT,
        http_retries: int = DEFAULT_HTTP_RETRIES,
        http_timeout: float = DEFAULT_HTTP_TIMEOUT,
        open_timeout: int = DEFAULT_WS_OPEN_TIMEOUT,
        close_timeout: int = DEFAULT_WS_CLOSE_TIMEOUT,
        _api_version: str = DEFAULT_API_VERSION,
        _api_http_base_url: str = DEFAULT_API_HTTP_BASE_URL,
        _api_ws_base_uri: str = DEFAULT_API_WS_BASE_URI,
    ) -> None:
        """Construct a Hume API client.

        Args:
            api_key (str): Hume API key.

            page_size (int): Number of items to return per page.
            retry_backoff_factor (float): Backoff factor to use for exponential backoff during request retries.
            retry_timeout (float): Maximum time in seconds to retry a request.
            http_retries (int): Maximum number of times to retry a request.
            http_timeout (float): Time in seconds before canceling an HTTP request.
            open_timeout (int): Time in seconds before canceling a socket open operation.
            close_timeout (int): Time in seconds before canceling a socket close operation.
        """
        self._api_key = api_key
        self._page_size = page_size
        self._retry_backoff_factor = retry_backoff_factor
        self._retry_timeout = retry_timeout
        self._http_retries = http_retries
        self._http_timeout = http_timeout
        self._open_timeout = open_timeout
        self._close_timeout = close_timeout

        self._api_version = _api_version
        self._api_http_base_url = _api_http_base_url
        self._api_ws_base_uri = _api_ws_base_uri

        transport = HTTPTransport(http2=True, retries=self._http_retries)
        self._http_client = HttpClient(
            follow_redirects=True,
            timeout=http_timeout,
            transport=transport,
        )

    def _request(
        self,
        endpoint: str,
        *,
        method: str,
        body_json_str: Optional[str] = None,
        paging: Optional[Paging] = None,
    ) -> Response:
        headers = self._get_client_headers()

        if body_json_str is None:
            content = None
        else:
            headers["Content-Type"] = "application/json"
            content = body_json_str.encode(encoding="utf-8")

        params = {}
        if paging is not None:
            if paging.page_size is not None:
                params["page_size"] = paging.page_size
            if paging.page_number != 0:
                params["page_number"] = paging.page_number

        request = self._http_client.build_request(
            method,
            endpoint,
            content=content,
            params=params,
            headers=headers,
        )

        try:
            response = self._http_client.send(request)
            response.raise_for_status()
        except Exception as exc:  # pylint: disable=broad-exception-caught
            response_body = response.json()
            if "message" in response_body:
                raise HumeClientException(response_body["message"]) from exc
            raise HumeClientException(str(response_body)) from exc

        return response

    def _get_client_headers(self) -> Dict[str, str]:
        return {
            "X-Hume-Api-Key": self._api_key,
            "X-Hume-Client-Name": "python_sdk",
            "X-Hume-Client-Version": version("hume"),
        }

    def _build_endpoint(
        self,
        service: str,
        path: str,
        protocol: str = Protocol.HTTP,
    ) -> str:
        if protocol == Protocol.HTTP:
            base = self._api_http_base_url
        elif protocol == Protocol.WS:
            base = self._api_ws_base_uri

        return f"{base}/{self._api_version}/{service}/{path}"
