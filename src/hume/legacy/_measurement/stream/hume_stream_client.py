"""Streaming API client."""

from __future__ import annotations

from collections.abc import Iterable
from contextlib import asynccontextmanager
from typing import Any, AsyncIterator

import websockets

from hume.legacy._common.client_base import ClientBase
from hume.legacy._common.protocol import Protocol
from hume.legacy._common.utilities.config_utilities import deserialize_configs
from hume.legacy._measurement.stream.stream_socket import StreamSocket
from hume.legacy.error.hume_client_exception import HumeClientException
from hume.legacy.models.config.model_config_base import ModelConfigBase


class HumeStreamClient(ClientBase):
    """Streaming API client.

    Example:
        ```python
        import asyncio

        from hume import HumeStreamClient
        from hume.models.config import BurstConfig
        from hume.models.config import ProsodyConfig

        async def main():
            client = HumeStreamClient("<your-api-key>")
            configs = [BurstConfig(), ProsodyConfig()]
            async with client.connect(configs) as socket:
                result = await socket.send_file("<your-audio-filepath>")
                print(result)

        asyncio.run(main())
        ```
    """

    @asynccontextmanager
    async def connect(
        self,
        configs: Iterable[ModelConfigBase],
        stream_window_ms: int | None = None,
    ) -> AsyncIterator[StreamSocket]:
        """Connect to the streaming API.

        Note: Only one config per model type should be passed.
            If more than one config is passed for a given model type, only the last config will be used.

        Args:
            configs (Iterable[ModelConfigBase]): List of job configs.
            stream_window_ms (int | None): Length of the sliding window in milliseconds to use when
                aggregating media across streaming payloads within one WebSocket connection.
        """
        endpoint = self._build_endpoint("stream", "models", protocol=Protocol.WS)
        try:
            # pylint: disable=no-member
            async with websockets.connect(  # type: ignore[attr-defined]
                endpoint,
                extra_headers=self._get_client_headers(),
                close_timeout=self._close_timeout,
                open_timeout=self._open_timeout,
            ) as protocol:
                yield StreamSocket(protocol, list(configs), stream_window_ms=stream_window_ms)
        except websockets.exceptions.InvalidStatusCode as exc:
            status_code: int = exc.status_code
            if status_code == 401:  # Unauthorized
                message = "HumeStreamClient initialized with invalid API key."
                raise HumeClientException(message) from exc
            raise HumeClientException("Unexpected error when creating streaming connection") from exc

    @asynccontextmanager
    async def _connect_with_configs_dict(self, configs_dict: Any) -> AsyncIterator[StreamSocket]:
        """Connect to the streaming API with a single models configuration dict.

        Args:
            configs_dict (Any): Models configurations dict. This should be a dict from model name
                to model configuration dict. An empty dict uses the default configuration.
        """
        configs = deserialize_configs(configs_dict)
        async with self.connect(configs) as websocket:
            yield websocket
