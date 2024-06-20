"""Empathic Voice Interface client."""

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
    auth_string = f"{api_key}:{secret_key}"
    return base64.b64encode(auth_string.encode()).decode()


def fetch_access_token(client_id: str, host: str = "api.hume.ai", timeout: int = 5) -> str:
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
    """Empathic Voice Interface client."""

    def __init__(self, api_key: str, secret_key: Optional[str] = None, enable_audio: bool = True, **kwargs: Any):
        super().__init__(api_key, enable_audio=enable_audio, **kwargs)
        self._token = None
        if secret_key:
            client_id = generate_client_id(api_key, secret_key)
            self._token = fetch_access_token(client_id)

    def _get_client_headers(self) -> dict[str, str]:
        headers = {
            "X-Hume-Client-Name": "python_sdk",
            "X-Hume-Client-Version": version("hume"),
        }
        if self._token:
            headers["Authorization"] = f"Bearer {self._token}"
        else:
            headers["X-Hume-Api-Key"] = self._api_key
        return headers
