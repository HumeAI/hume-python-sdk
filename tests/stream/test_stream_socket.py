from unittest.mock import Mock

import pytest
from pytest import TempPathFactory

from hume import HumeClientError, StreamSocket
from hume.config import FaceConfig, FacemeshConfig, LanguageConfig, ProsodyConfig


@pytest.mark.asyncio
@pytest.mark.stream
class TestStreamSocket:

    async def test_send_bytes_str(self, mock_face_protocol: Mock):
        configs = [FaceConfig(identify_faces=True)]
        socket = StreamSocket(mock_face_protocol, configs)
        mock_bytes_str = "bW9jay1tZWRpYS1maWxl"
        result = await socket._send_bytes_str(mock_bytes_str)
        assert result["face"]["predictions"] == "mock-predictions"

    async def test_send_bytes(self, mock_face_protocol: Mock):
        configs = [FaceConfig(identify_faces=True)]
        socket = StreamSocket(mock_face_protocol, configs)
        mock_bytes = b'bW9jay1tZWRpYS1maWxl'
        result = await socket.send_bytes(mock_bytes)
        assert result["face"]["predictions"] == "mock-predictions"

    async def test_send_file(self, mock_face_protocol: Mock, tmp_path_factory: TempPathFactory):
        configs = [FaceConfig(identify_faces=True)]
        socket = StreamSocket(mock_face_protocol, configs)

        media_data = "mock-media-file"
        media_filepath = tmp_path_factory.mktemp("data") / "data.txt"
        with media_filepath.open("w") as f:
            f.write(media_data)

        result = await socket.send_file(media_filepath)
        assert result["face"]["predictions"] == "mock-predictions"

    async def test_send_text(self, mock_language_protocol: Mock):
        configs = [LanguageConfig()]
        socket = StreamSocket(mock_language_protocol, configs)

        sample_text = "mock-text"
        result = await socket.send_text(sample_text)
        assert result["language"]["predictions"] == "mock-predictions"

    async def test_send_text_not_language(self, mock_language_protocol: Mock):
        configs = [ProsodyConfig()]
        socket = StreamSocket(mock_language_protocol, configs)

        sample_text = "mock-text"
        message = ("Socket configured with ProsodyConfig. "
                   "send_text is only supported when using a `LanguageConfig`")
        with pytest.raises(HumeClientError, match=message):
            await socket.send_text(sample_text)

    async def test_send_facemesh(self, mock_facemesh_protocol: Mock):
        configs = [FacemeshConfig()]
        socket = StreamSocket(mock_facemesh_protocol, configs)

        sample_facemesh = "mock-facemesh"
        result = await socket.send_facemesh(sample_facemesh)
        assert result["facemesh"]["predictions"] == "mock-predictions"

    async def test_send_facemesh_not_facemesh(self, mock_language_protocol: Mock):
        configs = [ProsodyConfig()]
        socket = StreamSocket(mock_language_protocol, configs)

        sample_facemesh = "mock-facemesh"
        message = ("Socket configured with ProsodyConfig. "
                   "send_facemesh is only supported when using a `FacemeshConfig`")
        with pytest.raises(HumeClientError, match=message):
            await socket.send_facemesh(sample_facemesh)
