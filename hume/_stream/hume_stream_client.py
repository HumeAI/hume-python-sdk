"""Streaming API client."""
import logging
from contextlib import asynccontextmanager
from typing import Any, AsyncIterator, List, Optional

from hume._common.api_type import ApiType
from hume._common.client_base import ClientBase
from hume._common.config_utils import configs_from_dict
from hume._stream.stream_socket import StreamSocket
from hume.error.hume_client_exception import HumeClientException
from hume.models.config import ModelConfigBase

try:
    import websockets
    HAS_WEBSOCKETS = True
except ModuleNotFoundError:
    HAS_WEBSOCKETS = False

logger = logging.getLogger(__name__)


class HumeStreamClient(ClientBase):
    """Streaming API client.

    Example:
        ```python
        import asyncio

        from hume import HumeStreamClient, StreamSocket
        from hume.models.config import FaceConfig

        async def main():
            client = HumeStreamClient("<your-api-key>")
            configs = [FaceConfig(identify_faces=True)]
            async with client.connect(configs) as socket:
                socket: StreamSocket
                result = await socket.send_file("<your-image-filepath>")
                print(result)

        asyncio.run(main())
        ```
    """

    _DEFAULT_API_TIMEOUT = 10

    def __init__(self, api_key: str, *args: Any, **kwargs: Any):
        """Construct a HumeStreamClient.

        Args:
            api_key (str): Hume API key.
        """
        if not HAS_WEBSOCKETS:
            raise HumeClientException("The websockets package is required to use HumeStreamClient. "
                                      "Run `pip install hume[stream]` to install a version compatible with the"
                                      "Hume Python SDK.")

        super().__init__(api_key, *args, _api_type=ApiType.STREAM, **kwargs)

    @asynccontextmanager
    async def connect(
        self,
        configs: List[ModelConfigBase],
        stream_window_ms: Optional[int] = None,
    ) -> AsyncIterator:
        """Connect to the streaming API.

        Note: Only one config per model type should be passed.
            If more than one config is passed for a given model type, only the last config will be used.

        Args:
            configs (List[ModelConfigBase]): List of job configs.
            stream_window_ms (Optional[int]): Length of the sliding window in milliseconds to use when
                aggregating media across streaming payloads within one websocket connection.
        """
        endpoint = self._construct_endpoint("models")
        try:
            # pylint: disable=no-member
            async with websockets.connect(  # type: ignore[attr-defined]
                    endpoint, extra_headers=self._get_client_headers()) as protocol:
                yield StreamSocket(protocol, configs, stream_window_ms=stream_window_ms)
        # TODO: Check for a 401 unauthorized
        except websockets.exceptions.InvalidStatusCode as exc:
            message = "HumeStreamClient initialized with invalid API key"
            raise HumeClientException(message) from exc

    @asynccontextmanager
    async def _connect_with_configs_dict(self, configs_dict: Any) -> AsyncIterator:
        """Connect to the streaming API with a single models configuration dict.

        Args:
            configs_dict (Any): Models configurations dict. This should be a dict from model name
                to model configuration dict. An empty dict uses the default configuration.
        """
        configs = configs_from_dict(configs_dict)
        async with self.connect(configs) as websocket:
            yield websocket
