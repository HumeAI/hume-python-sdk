"""Base class for Hume clients."""
from abc import ABC, abstractmethod
from importlib.metadata import version
from typing import Dict

from hume._common.api_type import ApiType


class ClientBase(ABC):
    """Base class for Hume API clients."""

    def __init__(
        self,
        api_key: str,
        _api_version: str = "v0",
        _api_http_base_url: str = "https://api.hume.ai",
        _api_ws_base_uri: str = "wss://api.hume.ai",
    ):
        """Construct a new Hume API client.

        Args:
            api_key (str): Hume API key.
        """
        self._api_key = api_key
        self._api_version = _api_version
        self._api_http_base_url = _api_http_base_url
        self._api_ws_base_uri = _api_ws_base_uri

    @classmethod
    @abstractmethod
    def get_api_type(cls) -> ApiType:
        """Get the ApiType of the client.

        Returns:
            ApiType: API type of the client.
        """

    def _get_client_headers(self) -> Dict[str, str]:
        package_version = version("hume")
        return {
            "X-Hume-Api-Key": self._api_key,
            "X-Hume-Client-Name": "python_sdk",
            "X-Hume-Client-Version": package_version,
        }

    def _construct_endpoint(self, path: str) -> str:
        api_type = self.get_api_type()
        base = self._api_ws_base_uri if api_type == ApiType.STREAM else self._api_http_base_url
        return f"{base}/{self._api_version}/{api_type.value}/{path}"
