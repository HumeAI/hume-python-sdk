import json
from unittest.mock import Mock

import pytest
from pytest import TempPathFactory

from hume import StreamSocket
from hume._common.config import FaceConfig


@pytest.fixture(scope="function")
def mock_protocol():

    async def mock_send(message: str) -> None:
        assert json.loads(message) == {
            "data": "bW9jay1tZWRpYS1maWxl",
            "models": {
                "face": {
                    "fps_pred": None,
                    "prob_threshold": None,
                    "identify_faces": True,
                    "min_face_size": None
                },
            },
        }

    async def mock_recv() -> str:
        return json.dumps({
            "face": {
                "predictions": "mock-predictions",
            },
        })

    protocol = Mock()
    protocol.send = mock_send
    protocol.recv = mock_recv
    return protocol


@pytest.mark.asyncio
@pytest.mark.stream
class TestStreamSocket:

    async def test_send_bytes_str(self, mock_protocol: Mock):
        configs = [FaceConfig(identify_faces=True)]
        socket = StreamSocket(mock_protocol, configs)
        mock_bytes_str = "bW9jay1tZWRpYS1maWxl"
        result = await socket.send_bytes_str(mock_bytes_str)
        assert result["face"]["predictions"] == "mock-predictions"

    async def test_send_bytes(self, mock_protocol: Mock):
        configs = [FaceConfig(identify_faces=True)]
        socket = StreamSocket(mock_protocol, configs)
        mock_bytes = b'bW9jay1tZWRpYS1maWxl'
        result = await socket.send_bytes(mock_bytes)
        assert result["face"]["predictions"] == "mock-predictions"

    async def test_send_file(self, mock_protocol: Mock, tmp_path_factory: TempPathFactory):
        configs = [FaceConfig(identify_faces=True)]
        socket = StreamSocket(mock_protocol, configs)

        media_data = "mock-media-file"
        media_filepath = tmp_path_factory.mktemp("data") / "data.txt"
        with media_filepath.open("w") as f:
            f.write(media_data)

        result = await socket.send_file(media_filepath)
        assert result["face"]["predictions"] == "mock-predictions"
