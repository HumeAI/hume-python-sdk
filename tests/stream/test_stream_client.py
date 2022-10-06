from contextlib import asynccontextmanager
from unittest.mock import Mock

import pytest
import websockets
from pytest import MonkeyPatch

from hume import HumeStreamClient, StreamSocket
from hume._common.config import FaceConfig


def mock_connect(uri: str):
    assert uri == "wss://api.hume.ai/v0/stream/multi?apikey=0000-0000-0000-0000"

    @asynccontextmanager
    async def mock_connection() -> Mock:
        yield Mock()

    return mock_connection()


@pytest.fixture(scope="function")
def stream_client() -> HumeStreamClient:
    return HumeStreamClient("0000-0000-0000-0000")


@pytest.mark.asyncio
@pytest.mark.stream
class TestHumeStreamClient:

    async def test_connect(self, stream_client: HumeStreamClient, monkeypatch: MonkeyPatch):
        monkeypatch.setattr(websockets, "connect", mock_connect)
        configs = [FaceConfig(identify_faces=True)]
        async with stream_client.connect(configs) as websocket:
            assert isinstance(websocket, StreamSocket)

    async def test_connect_to_models(self, stream_client: HumeStreamClient, monkeypatch: MonkeyPatch):
        monkeypatch.setattr(websockets, "connect", mock_connect)
        configs_dict = {
            "face": {
                "identify_faces": True,
            },
        }
        async with stream_client._connect_to_models(configs_dict) as websocket:
            assert isinstance(websocket, StreamSocket)
