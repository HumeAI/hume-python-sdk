"""Base class for Hume clients."""
from abc import ABC
from typing import Dict, Optional
import importlib.metadata


class ClientBase(ABC):
    """Base class for Hume API clients."""

    _HTTP_BASE_URL = "https://api.hume.ai"
    _WS_BASE_URI = "wss://api.hume.ai"

    def __init__(
        self,
        api_key: str,
        _api_version: str = "v0",
        _api_http_base_url: Optional[str] = None,
        _api_ws_base_uri: Optional[str] = None,
    ):
        """Construct a new Hume API client.

        Args:
            api_key (str): Hume API key.
        """
        self._api_key = api_key
        self._api_version = _api_version
        self._api_http_base_url = self._HTTP_BASE_URL if _api_http_base_url is None else _api_http_base_url
        self._api_ws_base_uri = self._WS_BASE_URI if _api_ws_base_uri is None else _api_ws_base_uri

    def _get_client_headers(self) -> Dict[str, str]:
        package_version = importlib.metadata.version("hume")
        return {
            "X-Hume-Client-Name": "python-sdk",
            "X-Hume-Client-Version": package_version,
            "X-Hume-Api-Key": self._api_key,
        }
