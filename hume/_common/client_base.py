"""Base class for Hume clients."""
from abc import ABC
from typing import Dict
import importlib.metadata

from hume._common.api_type import ApiType


class ClientBase(ABC):
    """Base class for Hume API clients."""

    def __init__(
        self,
        api_key: str,
        _api_type: ApiType = ApiType.BATCH,
        _api_version: str = "v0",
        _api_http_base_url: str = "https://api.hume.ai",
        _api_ws_base_uri: str = "wss://api.hume.ai",
    ):
        """Construct a new Hume API client.

        Args:
            api_key (str): Hume API key.
        """
        self._api_key = api_key
        self._api_type = _api_type
        self._api_version = _api_version
        self._api_http_base_url = _api_http_base_url
        self._api_ws_base_uri = _api_ws_base_uri

    def _get_client_headers(self) -> Dict[str, str]:
        package_version = importlib.metadata.version("hume")
        return {
            "X-Hume-Client-Name": "python-sdk",
            "X-Hume-Client-Version": package_version,
            "X-Hume-Api-Key": self._api_key,
        }

    def _construct_endpoint(self, path: str) -> str:
        base = self._api_ws_base_uri if self._api_type == ApiType.STREAM else self._api_http_base_url
        return f"{base}/{self._api_version}/{self._api_type.value}/{path}"
