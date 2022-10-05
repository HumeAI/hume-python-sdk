"""Streaming API client."""
import logging
from contextlib import asynccontextmanager
from typing import Any, AsyncIterator, List

from hume._common.api_type import ApiType
from hume._common.client_base import ClientBase
from hume._common.config import JobConfigBase
from hume._common.config.config_utils import config_from_model_type
from hume._common.hume_client_error import HumeClientError
from hume._common.model_type import ModelType
from hume._stream.stream_socket import StreamSocket

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
        from hume.config import FaceConfig

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

    def __init__(self, *args: Any, **kwargs: Any):
        """Construct a HumeStreamClient.

        Args:
            api_key (str): Hume API key.
        """
        if not HAS_WEBSOCKETS:
            raise HumeClientError("websockets package required to use HumeStreamClient")

        super().__init__(*args, **kwargs)

    @asynccontextmanager
    async def connect(self, configs: List[JobConfigBase]) -> AsyncIterator:
        """Connect to the streaming API.

        Args:
            configs (List[JobConfigBase]): List of job configs.
        """
        uri = (f"{self._api_ws_base_uri}/{self._api_version}/{ApiType.STREAM.value}/multi"
               f"?apikey={self._api_key}")

        try:
            # pylint: disable=no-member
            async with websockets.connect(uri) as protocol:  # type: ignore[attr-defined]
                yield StreamSocket(protocol, configs)
        except websockets.exceptions.InvalidStatusCode as exc:
            message = "Client initialized with invalid API key"
            raise HumeClientError(message) from exc

    @asynccontextmanager
    async def _connect_to_models(self, configs_dict: Any) -> AsyncIterator:
        """Connect to the streaming API with a single models configuration dict.

        Args:
            configs_dict (Any): Models configurations dict. This should be a dict from model name
                to model configuration dict. An empty dict uses the default configuration.
        """
        configs = []
        for model_name, config_dict in configs_dict.items():
            model_type = ModelType.from_str(model_name)
            config = config_from_model_type(model_type).deserialize(config_dict)
            configs.append(config)

        async with self.connect(configs) as websocket:
            yield websocket
