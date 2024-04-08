import re
from unittest.mock import Mock

import pytest
from pytest import TempPathFactory

from hume import HumeClientException, StreamSocket
from hume.models.config import FaceConfig, FacemeshConfig, LanguageConfig, ProsodyConfig


@pytest.mark.asyncio
@pytest.mark.stream
class TestStreamSocket:

    async def test_send_bytes_str(self, mock_face_protocol: Mock) -> None:
        configs = [FaceConfig(identify_faces=True)]
        socket = StreamSocket(mock_face_protocol, configs)
        mock_bytes_str = "bW9jay1tZWRpYS1maWxl"
        result = await socket._send_str(mock_bytes_str, raw_text=False)
        assert result["face"]["predictions"] == "mock-predictions"

    async def test_send_raw_str(self, mock_language_protocol: Mock) -> None:
        configs = [LanguageConfig()]
        socket = StreamSocket(mock_language_protocol, configs)
        mock_raw_str = "mock-text"
        result = await socket._send_str(mock_raw_str, raw_text=True)
        assert result["language"]["predictions"] == "mock-predictions"

    async def test_send_bytes(self, mock_face_protocol: Mock) -> None:
        configs = [FaceConfig(identify_faces=True)]
        socket = StreamSocket(mock_face_protocol, configs)
        mock_bytes = b"bW9jay1tZWRpYS1maWxl"
        result = await socket.send_bytes(mock_bytes)
        assert result["face"]["predictions"] == "mock-predictions"

    async def test_send_file(self, mock_face_protocol: Mock, tmp_path_factory: TempPathFactory) -> None:
        configs = [FaceConfig(identify_faces=True)]
        socket = StreamSocket(mock_face_protocol, configs)

        media_data = "mock-media-file"
        media_filepath = tmp_path_factory.mktemp("data") / "data.txt"
        with media_filepath.open("w") as f:
            f.write(media_data)

        result = await socket.send_file(media_filepath)
        assert result["face"]["predictions"] == "mock-predictions"

    async def test_send_text(self, mock_language_protocol: Mock) -> None:
        configs = [LanguageConfig()]
        socket = StreamSocket(mock_language_protocol, configs)

        sample_text = "mock-text"
        result = await socket.send_text(sample_text)
        assert result["language"]["predictions"] == "mock-predictions"

    async def test_send_text_not_language(self, mock_language_protocol: Mock) -> None:
        configs = [ProsodyConfig()]
        socket = StreamSocket(mock_language_protocol, configs)

        sample_text = "mock-text"
        message = "Socket configured with ProsodyConfig. send_text is only supported when using a LanguageConfig."
        with pytest.raises(HumeClientException, match=re.escape(message)):
            await socket.send_text(sample_text)

    async def test_send_facemesh(self, mock_facemesh_protocol: Mock) -> None:
        configs = [FacemeshConfig()]
        socket = StreamSocket(mock_facemesh_protocol, configs)

        sample_facemesh = [[[0, 0, 0]] * 478]
        result = await socket.send_facemesh(sample_facemesh)
        assert result["facemesh"]["predictions"] == "mock-predictions"

    async def test_send_facemesh_not_facemesh(self, mock_facemesh_protocol: Mock) -> None:
        configs = [ProsodyConfig()]
        socket = StreamSocket(mock_facemesh_protocol, configs)

        sample_facemesh = [[[0, 0, 0]] * 478]
        message = "Socket configured with ProsodyConfig. send_facemesh is only supported when using a FacemeshConfig."
        with pytest.raises(HumeClientException, match=re.escape(message)):
            await socket.send_facemesh(sample_facemesh)

    async def test_send_facemesh_array_shapes(self, mock_facemesh_protocol: Mock) -> None:
        configs = [FacemeshConfig()]
        socket = StreamSocket(mock_facemesh_protocol, configs)

        message = "No faces sent in facemesh payload."
        with pytest.raises(HumeClientException, match=re.escape(message)):
            await socket.send_facemesh([])

        message = "Number of faces sent in facemesh payload was greater than the limit of 100, found 150."
        with pytest.raises(HumeClientException, match=re.escape(message)):
            await socket.send_facemesh([0] * 150)

        message = "Number of MediaPipe landmarks per face must be exactly 478, found 474."
        with pytest.raises(HumeClientException, match=re.escape(message)):
            await socket.send_facemesh([[[0, 0, 0]] * 474])

        message = "Invalid facemesh payload detected. Each facemesh landmark should be an (x, y, z) point."
        with pytest.raises(HumeClientException, match=re.escape(message)):
            await socket.send_facemesh([[[0, 0]] * 478])

    async def test_invalid_payload_configs_send_text(self, mock_language_protocol: Mock) -> None:
        socket_configs = [LanguageConfig()]
        socket = StreamSocket(mock_language_protocol, socket_configs)

        sample_text = "mock-text"
        message = "Payload configured with ProsodyConfig. send_text is only supported when using a LanguageConfig."
        with pytest.raises(HumeClientException, match=re.escape(message)):
            payload_configs = [ProsodyConfig()]
            await socket.send_text(sample_text, configs=payload_configs)
