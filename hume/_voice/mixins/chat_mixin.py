from __future__ import annotations

import asyncio
import logging
import urllib.parse
from contextlib import asynccontextmanager
from typing import Any, AsyncIterator, ClassVar

import websockets
import websockets.client

from hume._common.client_base import ClientBase
from hume._common.protocol import Protocol
from hume._voice.voice_socket import VoiceSocket
from hume.error.hume_client_exception import HumeClientException

logger = logging.getLogger(__name__)


class ChatMixin(ClientBase):
    """Client operations for EVI WebSocket connections."""

    DEFAULT_MAX_PAYLOAD_SIZE_BYTES: ClassVar[int] = 2**24

    @asynccontextmanager
    async def connect(
        self,
        config_id: str | None = None,
        chat_group_id: str | None = None,
    ) -> AsyncIterator[VoiceSocket]:
        """Connect to the EVI API.

        Args:
            config_id (str | None): Config ID.
            chat_group_id (str | None): Chat group ID.
        """
        uri_base = self._build_endpoint("evi", "chat", Protocol.WS)

        if config_id is not None and chat_group_id is not None:
            raise HumeClientException(
                "If resuming from a chat_group_id you must not provide a config_id. "
                "The original config for the chat group will be used automatically."
            )

        params: dict[str, Any] = {}
        if config_id is not None:
            params["config_id"] = config_id
        if chat_group_id is not None:
            params["resumed_chat_group_id"] = chat_group_id

        encoded_params = urllib.parse.urlencode(params)
        uri = f"{uri_base}?{encoded_params}"

        logger.info("Connecting to EVI API at %s", uri)

        max_size = self.DEFAULT_MAX_PAYLOAD_SIZE_BYTES
        try:
            # pylint: disable=no-member
            async with websockets.connect(  # type: ignore[attr-defined]
                uri,
                extra_headers=self._get_client_headers(),
                close_timeout=self._close_timeout,
                open_timeout=self._open_timeout,
                max_size=max_size,
            ) as protocol:

                # await self._handle_open_close(on_open)
                # voice_socket = VoiceSocket(protocol)
                # byte_strs: Stream = Stream.new()
                # recv_task = asyncio.create_task(self._handle_messages(voice_socket, byte_strs, on_message, on_error))
                # self._audio_task = asyncio.create_task(self._audio_playback(byte_strs))
                # yield voice_socket
                # await asyncio.gather(recv_task, self._audio_task)

                async def do_nothing() -> None:
                    pass

                await do_nothing()

                voice_socket = VoiceSocket(protocol)

                do_nothing_task = asyncio.create_task(do_nothing())

                yield voice_socket

                await asyncio.gather(do_nothing_task)

        except websockets.exceptions.InvalidStatusCode as exc:
            status_code: int = exc.status_code
            if status_code == 401:  # Unauthorized
                message = "HumeVoiceClient initialized with invalid API key."
                raise HumeClientException(message) from exc
            raise HumeClientException("Unexpected error when creating EVI API connection") from exc
