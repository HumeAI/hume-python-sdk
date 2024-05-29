from contextlib import asynccontextmanager
from typing import AsyncContextManager, Dict, Optional
from unittest.mock import Mock

import pytest
import websockets
from pytest import MonkeyPatch

from hume import HumeStreamClient, StreamSocket
from hume.models.config import FaceConfig, ProsodyConfig


def mock_connect(
    uri: str,
    extra_headers: Optional[Dict[str, str]] = None,
    open_timeout: Optional[int] = None,
    close_timeout: Optional[int] = None,
) -> AsyncContextManager[Mock]:
    assert uri == "wss://api.hume.ai/v0/stream/models"
    assert isinstance(extra_headers, dict)
    assert extra_headers.get("X-Hume-Client-Name") == "python_sdk"
    assert extra_headers.get("X-Hume-Api-Key") is not None
    assert isinstance(extra_headers.get("X-Hume-Client-Version"), str)

    @asynccontextmanager
    async def mock_connection() -> Mock:
        yield Mock()

    return mock_connection()


@pytest.fixture(name="stream_client", scope="function")
def stream_client_fixture() -> HumeStreamClient:
    return HumeStreamClient("0000-0000-0000-0000")


@pytest.mark.asyncio
@pytest.mark.stream
class TestHumeStreamClient:

    async def test_connect_basic(self, stream_client: HumeStreamClient, monkeypatch: MonkeyPatch) -> None:
        monkeypatch.setattr(websockets, "connect", mock_connect)
        configs = [FaceConfig(identify_faces=True)]
        async with stream_client.connect(configs) as socket:
            assert isinstance(socket, StreamSocket)

    async def test_connect_stream_window_ms(self, stream_client: HumeStreamClient, monkeypatch: MonkeyPatch) -> None:
        monkeypatch.setattr(websockets, "connect", mock_connect)
        configs = [ProsodyConfig()]
        async with stream_client.connect(configs, stream_window_ms=350) as socket:
            assert socket._stream_window_ms == 350

    async def test_connect_with_models_config(self, stream_client: HumeStreamClient, monkeypatch: MonkeyPatch) -> None:
        monkeypatch.setattr(websockets, "connect", mock_connect)
        configs_dict = {
            "face": {
                "identify_faces": True,
            },
            "prosody": {},
        }
        async with stream_client._connect_with_configs_dict(configs_dict) as socket:
            assert len(socket._configs) == 2
