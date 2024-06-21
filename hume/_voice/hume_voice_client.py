"""Empathic Voice Interface client module."""

import base64
import logging
from importlib.metadata import version
from typing import Any, Optional

import httpx

from hume._voice.mixins.chat_mixin import ChatMixin
from hume._voice.mixins.chats_mixin import ChatsMixin
from hume._voice.mixins.configs_mixin import ConfigsMixin
from hume._voice.mixins.tools_mixin import ToolsMixin

logger = logging.getLogger(__name__)


def generate_client_id(api_key: str, secret_key: str) -> str:
    """Generate a Base64 encoded client ID from API key and secret key.

    Args:
        api_key (str): The API key provided by Hume.
        secret_key (str): The secret key provided by Hume.

    Returns:
        str: Base64 encoded client ID.
    """
    auth_string = f"{api_key}:{secret_key}"
    return base64.b64encode(auth_string.encode()).decode()


def fetch_access_token(client_id: str, host: str = "api.hume.ai", timeout: int = 5) -> str:
    """Fetch an access token using the client ID.

    Args:
        client_id (str): The Base64 encoded client ID.
        host (str): The Hume API host. Defaults to "api.hume.ai".
        timeout (int): Timeout for the HTTP request. Defaults to 5 seconds.

    Returns:
        str: Access token.

    Raises:
        ValueError: If the access token is not found in the response.
    """
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Basic {client_id}",
    }
    data = {
        "grant_type": "client_credentials",
    }
    with httpx.Client(timeout=timeout) as client:
        response = client.post(f"https://{host}/oauth2-cc/token", headers=headers, data=data)
        response_data = response.json()
    if "access_token" not in response_data:
        raise ValueError("Access token not found in response")
    return response_data["access_token"]


class HumeVoiceClient(ChatMixin, ChatsMixin, ConfigsMixin, ToolsMixin):
    """Empathic Voice Interface client.

    This client integrates with the Hume API to provide various EVI-related operations,
    including chat and configuration management.

    Attributes:
        _token (Optional[str]): The access token for authentication.
        enable_audio (bool): Flag indicating whether audio playback is enabled.
    """

    def __init__(self, api_key: str, secret_key: Optional[str] = None, **kwargs: Any):
        """
        Initialize the HumeVoiceClient.

        Args:
            api_key (str): The API key provided by Hume.
            secret_key (Optional[str]): The secret key provided by Hume. Required for token-based authentication.
            **kwargs: Additional arguments to pass to the parent class initializer.
        """
        super().__init__(api_key, **kwargs)
        self._token: Optional[str] = None
        if secret_key:
            client_id = generate_client_id(api_key, secret_key)
            self._token = fetch_access_token(client_id)

    def _get_client_headers(self) -> dict[str, str]:
        """
        Get the headers required for API requests.

        Returns:
            dict[str, str]: A dictionary of headers.
        """
        headers = {
            "X-Hume-Client-Name": "python_sdk",
            "X-Hume-Client-Version": version("hume"),
        }
        if self._token:
            headers["Authorization"] = f"Bearer {self._token}"
        else:
            headers["X-Hume-Api-Key"] = self._api_key
        return headers
