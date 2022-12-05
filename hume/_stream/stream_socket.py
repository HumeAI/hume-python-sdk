"""Streaming socket connection."""
import base64
import json
from pathlib import Path
from typing import Any, List, Union

try:
    from websockets.client import WebSocketClientProtocol
    HAS_WEBSOCKETS = True
except ModuleNotFoundError:
    HAS_WEBSOCKETS = False

from hume._common.config import JobConfigBase, LanguageConfig
from hume._common.hume_client_error import HumeClientError


class StreamSocket:
    """Streaming socket connection."""

    def __init__(
        self,
        protocol: "WebSocketClientProtocol",
        configs: List[JobConfigBase],
    ):
        """Construct a `StreamSocket`.

        Args:
            protocol (WebSocketClientProtocol): Protocol instance from websockets library.
            configs (List[JobConfigBase]): List of model configurations.

        Raises:
            HumeClientError: If there is an error processing media over the socket connection.
        """
        if not HAS_WEBSOCKETS:
            raise HumeClientError("websockets package required to use HumeStreamClient")

        self._configs = configs
        self._protocol = protocol

        self._serialized_configs = self._serialize_configs(configs)

    @classmethod
    def _serialize_configs(cls, configs: List[JobConfigBase]) -> Any:
        serialized = {}
        for config in configs:
            model_type = config.get_model_type()
            model_name = model_type.value
            serialized[model_name] = config.serialize()
        return serialized

    @classmethod
    def _file_to_bytes(cls, filepath: Path) -> bytes:
        with filepath.open('rb') as f:
            return base64.b64encode(f.read())

    def _get_predictions(self, response: str) -> Any:
        try:
            json_response = json.loads(response)
        except json.JSONDecodeError as exc:
            raise HumeClientError("Unexpected error when fetching streaming API predictions") from exc

        return json_response

    async def _send_bytes_str(self, bytes_str: str) -> Any:
        """Send raw bytes string on the `StreamSocket`.

        Note: Must be base64 encoded bytes.

        Args:
            bytes_str (str): Raw bytes of media to send on socket connection converted to a string.

        Returns:
            Any: Predictions from the streaming API.
        """
        payload = {
            "data": bytes_str,
            "models": self._serialized_configs,
        }
        json_payload = json.dumps(payload)
        await self._protocol.send(json_payload)
        response = await self._protocol.recv()
        # Cast to str because websockets can send bytes, but we will always accept JSON strings
        response_str = str(response)
        return self._get_predictions(response_str)

    async def send_bytes(self, bytes_data: bytes) -> Any:
        """Send raw bytes on the `StreamSocket`.

        Note: Must be base64 encoded bytes.

        Args:
            bytes_data (bytes): Raw bytes of media to send on socket connection.

        Returns:
            Any: Predictions from the streaming API.
        """
        bytes_str = bytes_data.decode("utf-8")
        return await self._send_bytes_str(bytes_str)

    async def send_file(self, filepath: Union[str, Path]) -> Any:
        """Send a file on the `StreamSocket`.

        Args:
            filepath (Path): Path to media file to send on socket connection.

        Returns:
            Any: Predictions from the streaming API.
        """
        bytes_data = self._file_to_bytes(Path(filepath))
        return await self.send_bytes(bytes_data)

    async def send_text(self, text: str) -> Any:
        """Send text on the `StreamSocket`.

        Note: This method is intended for use with a `LanguageConfig`.
            When the socket is configured for other modalities this method will fail.

        Args:
            text (str): Text to send to the language model.

        Raises:
            HumeClientError: If the socket is configured with a modality other than language.

        Returns:
            Any: Predictions from the streaming API.
        """
        for config in self._configs:
            if not isinstance(config, LanguageConfig):
                config_type = config.__class__.__name__
                raise HumeClientError(f"Socket configured with {config_type}. "
                                      "send_text is only supported when using a `LanguageConfig`")

        bytes_data = base64.b64encode(text.encode("utf-8"))
        return await self.send_bytes(bytes_data)
