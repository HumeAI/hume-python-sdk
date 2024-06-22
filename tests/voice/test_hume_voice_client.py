from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from typing import AsyncContextManager, AsyncIterator, Optional
from unittest.mock import Mock

import pytest
import websockets
from hume import HumeVoiceClient
from hume._voice.voice_socket import VoiceSocket
from pytest import MonkeyPatch

logger = logging.getLogger(__name__)


def mock_connect(
    uri: str,
    extra_headers: Optional[dict[str, str]] = None,
    _open_timeout: Optional[int] = None,
    _close_timeout: Optional[int] = None,
    max_size: Optional[int] = None,
) -> AsyncContextManager[Mock]:
    assert uri.startswith("wss://api.hume.ai/v0/evi/chat")
    assert isinstance(extra_headers, dict)
    assert extra_headers.get("X-Hume-Client-Name") == "python_sdk"
    assert extra_headers.get("X-Hume-Api-Key") is not None
    assert isinstance(extra_headers.get("X-Hume-Client-Version"), str)
    assert max_size == 16777216

    @asynccontextmanager
    async def mock_connection() -> AsyncIterator[Mock]:
        yield Mock()

    return mock_connection()


@pytest.fixture(name="voice_client", scope="function")
def voice_client_fixture() -> HumeVoiceClient:
    return HumeVoiceClient("0000-0000-0000-0000")


@pytest.mark.asyncio
@pytest.mark.voice
class TestHumeVoiceClient:
    async def test_connect_basic(self, voice_client: HumeVoiceClient, monkeypatch: MonkeyPatch) -> None:
        monkeypatch.setattr(websockets, "connect", mock_connect)
        async with voice_client.connect() as socket:
            assert isinstance(socket, VoiceSocket)
