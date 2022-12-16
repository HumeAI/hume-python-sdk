import json
from unittest.mock import Mock

import pytest


@pytest.fixture(scope="function")
def mock_face_protocol():

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


@pytest.fixture(scope="function")
def mock_language_protocol():

    async def mock_send(message: str) -> None:
        assert json.loads(message) == {
            "data": "bW9jay10ZXh0",
            "models": {
                "language": {
                    "identify_speakers": None,
                    "sliding_window": None,
                },
            },
        }

    async def mock_recv() -> str:
        return json.dumps({
            "language": {
                "predictions": "mock-predictions",
            },
        })

    protocol = Mock()
    protocol.send = mock_send
    protocol.recv = mock_recv
    return protocol


@pytest.fixture(scope="function")
def mock_facemesh_protocol():

    async def mock_send(message: str) -> None:
        assert json.loads(message) == {
            "data": "Im1vY2stZmFjZW1lc2gi",
            "models": {
                "facemesh": {},
            },
        }

    async def mock_recv() -> str:
        return json.dumps({
            "facemesh": {
                "predictions": "mock-predictions",
            },
        })

    protocol = Mock()
    protocol.send = mock_send
    protocol.recv = mock_recv
    return protocol
