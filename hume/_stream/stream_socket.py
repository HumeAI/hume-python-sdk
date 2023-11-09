"""Streaming socket connection."""
import base64
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from hume._common.config_utils import serialize_configs
from hume.error.hume_client_exception import HumeClientException
from hume.models.config import FacemeshConfig, LanguageConfig, ModelConfigBase

try:
    from websockets.client import WebSocketClientProtocol

    HAS_WEBSOCKETS = True
except ModuleNotFoundError:
    HAS_WEBSOCKETS = False


class StreamSocket:
    """Streaming socket connection."""

    _FACE_LIMIT = 100
    _N_LANDMARKS = 478
    _N_SPATIAL = 3

    def __init__(
        self,
        protocol: "WebSocketClientProtocol",
        configs: List[ModelConfigBase],
        stream_window_ms: Optional[int] = None,
    ):
        """Construct a `StreamSocket`.

        Args:
            protocol (WebSocketClientProtocol): Protocol instance from websockets library.
            configs (Optional[List[ModelConfigBase]]): List of model configurations.
            stream_window_ms (Optional[int]): Length of the sliding window in milliseconds to use when
                aggregating media across streaming payloads within one websocket connection.

        Raises:
            HumeClientException: If there is an error processing media over the socket connection.
        """
        if not HAS_WEBSOCKETS:
            raise HumeClientException(
                "The websockets package is required to use HumeStreamClient. "
                'Run `pip install "hume[stream]"` to install a version compatible with the'
                "Hume Python SDK."
            )

        self._protocol = protocol
        self._configs = configs
        self._stream_window_ms = stream_window_ms

        # Serialize configs once for full lifetime of socket
        self._serialized_configs = serialize_configs(configs)

    async def send_file(
        self,
        filepath: Union[str, Path],
        configs: Optional[List[ModelConfigBase]] = None,
    ) -> Any:
        """Send a file on the `StreamSocket`.

        Args:
            filepath (Path): Path to media file to send on socket connection.
            configs (Optional[List[ModelConfigBase]]): List of model configurations.
                If set these configurations will overwrite any configurations
                set when initializing the `StreamSocket`.

        Returns:
            Any: Response from the streaming API.
        """
        with Path(filepath).open("rb") as f:
            bytes_data = base64.b64encode(f.read())
            return await self.send_bytes(bytes_data, configs=configs)

    async def send_bytes(
        self,
        bytes_data: bytes,
        configs: Optional[List[ModelConfigBase]] = None,
    ) -> Any:
        """Send raw bytes on the `StreamSocket`.

        Note: Input should be base64 encoded bytes.
            You can use base64.b64encode() to encode a raw string.

        Args:
            bytes_data (bytes): Raw bytes of media to send on socket connection.
            configs (Optional[List[ModelConfigBase]]): List of model configurations.
                If set these configurations will overwrite any configurations
                set when initializing the `StreamSocket`.

        Returns:
            Any: Response from the streaming API.
        """
        bytes_str = bytes_data.decode("utf-8")
        return await self._send_str(bytes_str, raw_text=False, configs=configs)

    async def send_text(
        self,
        text: str,
        configs: Optional[List[ModelConfigBase]] = None,
    ) -> Any:
        """Send text on the `StreamSocket`.

        Note: This method is intended for use with a `LanguageConfig`.
            When the socket is configured for other modalities this method will fail.

        Args:
            text (str): Text to send to the language model.
            configs (Optional[List[ModelConfigBase]]): List of model configurations.
                If set these configurations will overwrite any configurations
                set when initializing the `StreamSocket`.

        Raises:
            HumeClientException: If the socket is configured with a modality other than language.

        Returns:
            Any: Response from the streaming API.
        """
        self._validate_configs_with_model_type(LanguageConfig, "send_text", configs=configs)
        return await self._send_str(text, raw_text=True, configs=configs)

    async def send_facemesh(
        self,
        landmarks: List[List[List[float]]],
        configs: Optional[List[ModelConfigBase]] = None,
    ) -> Any:
        """Send facemesh landmarks on the `StreamSocket`.

        Note: This method is intended for use with a `FacemeshConfig`.
            When the socket is configured for other modalities this method will fail.

        Args:
            landmarks (List[List[List[float]]]): List of landmark points for multiple faces.
                The shape of this 3-dimensional list should be (n, 478, 3) where n is the number
                of faces to be processed, 478 is the number of MediaPipe landmarks per face and 3
                represents the (x, y, z) coordinates of each landmark.
            configs (Optional[List[ModelConfigBase]]): List of model configurations.
                If set these configurations will overwrite any configurations
                set when initializing the `StreamSocket`.

        Raises:
            HumeClientException: If the socket is configured with a modality other than facemesh.

        Returns:
            Any: Response from the streaming API.
        """
        self._validate_configs_with_model_type(FacemeshConfig, "send_facemesh", configs=configs)

        n_faces = len(landmarks)
        if n_faces > self._FACE_LIMIT:
            raise HumeClientException(
                "Number of faces sent in facemesh payload was greater "
                f"than the limit of {self._FACE_LIMIT}, found {n_faces}."
            )
        if n_faces == 0:
            raise HumeClientException("No faces sent in facemesh payload.")
        n_landmarks = len(landmarks[0])
        if n_landmarks != self._N_LANDMARKS:
            raise HumeClientException(
                f"Number of MediaPipe landmarks per face must be exactly {self._N_LANDMARKS}, " f"found {n_landmarks}."
            )
        if len(landmarks[0][0]) != self._N_SPATIAL:
            raise HumeClientException(
                "Invalid facemesh payload detected. Each facemesh landmark should be an (x, y, z) point."
            )

        landmarks_str = json.dumps(landmarks)
        bytes_data = base64.b64encode(landmarks_str.encode("utf-8"))
        return await self.send_bytes(bytes_data, configs=configs)

    async def reset_stream(self) -> Any:
        """Reset the streaming sliding window.

        A sliding window of context is maintained for the lifetime of your streaming connection.
        Call this method when some media has been fully processed and you want to continue using the same
        streaming connection without leaking context across media samples.

        Returns:
            Any: Response from the streaming API.
        """
        payload = {
            "reset_stream": True,
        }
        return await self._send_payload(payload)

    async def get_job_details(self) -> Any:
        """Get details associated with the current streaming connection.

        Returns:
            Any: Response from the streaming API.
        """
        payload = {
            "job_details": True,
        }
        return await self._send_payload(payload)

    async def _send_str(
        self,
        data: str,
        *,
        raw_text: bool,
        configs: Optional[List[ModelConfigBase]] = None,
    ) -> Any:
        serialized_configs = self._serialized_configs
        if configs is not None:
            serialized_configs = serialize_configs(configs)

        payload: Dict[str, Any] = {
            "data": data,
            "models": serialized_configs,
            "raw_text": raw_text,
        }
        if self._stream_window_ms is not None:
            payload["stream_window_ms"] = self._stream_window_ms
        return await self._send_payload(payload)

    async def _send_payload(self, payload: Dict[str, Any]) -> Any:
        request_message = json.dumps(payload)
        await self._protocol.send(request_message)
        response_data = await self._protocol.recv()
        # Cast to str because websockets can send bytes, but we will always accept JSON strings
        response_str = str(response_data)

        try:
            response = json.loads(response_str)
        except json.JSONDecodeError as exc:
            raise HumeClientException("Unexpected error when fetching streaming API predictions") from exc

        if "error" in response:
            error = response["error"]
            code = response["code"]
            raise HumeClientException.from_error(code, error)

        return response

    def _validate_configs_with_model_type(
        self,
        config_type: Any,
        method_name: str,
        configs: Optional[List[ModelConfigBase]] = None,
    ) -> None:
        config_method = "Socket"
        payload_configs = self._configs
        if configs is not None:
            config_method = "Payload"
            payload_configs = configs

        for config in payload_configs:
            if not isinstance(config, config_type):
                config_name = config_type.__name__
                invalid_config_name = config.__class__.__name__
                raise HumeClientException(
                    f"{config_method} configured with {invalid_config_name}. "
                    f"{method_name} is only supported when using a {config_name}."
                )
