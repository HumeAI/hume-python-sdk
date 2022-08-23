"""Base class for Hume clients."""
from typing import Optional
from abc import ABC


class ClientBase(ABC):
    """Base class for Hume API clients."""

    _API_BASE_URL = "https://api.hume.ai"

    def __init__(
        self,
        api_key: str,
        _api_version: str = "v0",
        _api_base_url: Optional[str] = None,
    ):
        """Construct a new Hume API client.

        Args:
            api_key (str): Hume API key.
        """
        self._api_key = api_key
        self._api_version = _api_version
        self._api_base_url = self._API_BASE_URL if _api_base_url is None else _api_base_url
