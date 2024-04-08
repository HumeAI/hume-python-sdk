import json
from unittest.mock import Mock

import pytest


@pytest.fixture(scope="function")
def mock_face_protocol() -> Mock:

    async def mock_send(message: str) -> None:
        assert json.loads(message) == {
            "data": "bW9jay1tZWRpYS1maWxl",
            "models": {
                "face": {
                    "identify_faces": True,
                },
            },
            "raw_text": False,
        }

    async def mock_recv() -> str:
        return json.dumps(
            {
                "face": {
                    "predictions": "mock-predictions",
                },
            }
        )

    protocol = Mock()
    protocol.send = mock_send
    protocol.recv = mock_recv
    return protocol


@pytest.fixture(scope="function")
def mock_language_protocol() -> Mock:

    async def mock_send(message: str) -> None:
        assert json.loads(message) == {
            "data": "mock-text",
            "models": {
                "language": {},
            },
            "raw_text": True,
        }

    async def mock_recv() -> str:
        return json.dumps(
            {
                "language": {
                    "predictions": "mock-predictions",
                },
            }
        )

    protocol = Mock()
    protocol.send = mock_send
    protocol.recv = mock_recv
    return protocol


@pytest.fixture(scope="function")
def mock_facemesh_protocol() -> Mock:

    async def mock_send(message: str) -> None:
        message_json = json.loads(message)
        assert message_json == {
            "data": message_json["data"],
            "models": {
                "facemesh": {},
            },
            "raw_text": False,
        }

    async def mock_recv() -> str:
        return json.dumps(
            {
                "facemesh": {
                    "predictions": "mock-predictions",
                },
            }
        )

    protocol = Mock()
    protocol.send = mock_send
    protocol.recv = mock_recv
    return protocol
