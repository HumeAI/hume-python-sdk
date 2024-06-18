import asyncio
import base64
import json
import logging
import urllib.parse
from contextlib import asynccontextmanager
from typing import Any, AsyncIterator, Awaitable, Callable, ClassVar, Dict, Optional, Union

import websockets
import websockets.client

from hume._common.client_base import ClientBase
from hume._common.protocol import Protocol
from hume._voice.microphone.asyncio_utilities import Stream
from hume._voice.microphone.audio_utilities import AudioPlayer
from hume._voice.voice_socket import VoiceSocket
from hume.error.hume_client_exception import HumeClientException

logger = logging.getLogger(__name__)

OpenCloseHandlerType = Union[Callable[[], None], Callable[[], Awaitable[None]]]
MessageHandlerType = Union[Callable[[dict], None], Callable[[dict], Awaitable[None]]]
ErrorHandlerType = Union[Callable[[Exception], None], Callable[[Exception], Awaitable[None]]]


class ChatMixin(ClientBase):
    """Client operations for EVI WebSocket connections."""

    DEFAULT_MAX_PAYLOAD_SIZE_BYTES: ClassVar[int] = 2**24

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.audio_player: AudioPlayer = AudioPlayer()
        self._audio_task: Optional[asyncio.Task] = None

    async def _handle_messages(
        self,
        voice_socket: VoiceSocket,
        byte_strs: Stream,
        on_message: Optional[MessageHandlerType],
        interruptible: bool,
        on_error: Optional[ErrorHandlerType],
    ) -> None:
        try:
            async for socket_message in voice_socket:
                message = json.loads(socket_message)
                await self._process_message(message, byte_strs, on_message, interruptible)
        except Exception as exc:
            await self._handle_error(exc, on_error)
            raise

    async def _process_message(
        self, message: dict, byte_strs: Stream, on_message: Optional[MessageHandlerType], interruptible: bool
    ) -> None:
        if message["type"] == "audio_output":
            message_str: str = message["data"]
            message_bytes = base64.b64decode(message_str.encode("utf-8"))
            await byte_strs.put(message_bytes)
        elif interruptible and message["type"] == "user_interruption":
            logger.debug("Received user_interruption message")
            self.audio_player.stop_audio()
        elif on_message is not None:
            if asyncio.iscoroutinefunction(on_message):
                await on_message(message)
            else:
                on_message(message)

    async def _audio_playback(self, byte_strs: Stream) -> None:
        async for byte_str in byte_strs:
            await self.audio_player.play_audio(byte_str)

    async def _handle_error(self, exc: Exception, on_error: Optional[ErrorHandlerType]) -> None:
        if on_error is not None:
            if asyncio.iscoroutinefunction(on_error):
                await on_error(exc)
            else:
                on_error(exc)

    async def _handle_open_close(self, handler: Optional[OpenCloseHandlerType]) -> None:
        if handler is not None:
            if asyncio.iscoroutinefunction(handler):
                await handler()
            else:
                handler()

    @asynccontextmanager
    async def connect(
        self,
        config_id: Optional[str] = None,
        resumed_chat_group_id: Optional[str] = None,
        on_open: Optional[OpenCloseHandlerType] = None,
        on_close: Optional[OpenCloseHandlerType] = None,
        on_error: Optional[ErrorHandlerType] = None,
        on_message: Optional[MessageHandlerType] = None,
        interruptible: bool = True,
    ) -> AsyncIterator[VoiceSocket]:
        """Connect to the EVI API.

        Args:
            config_id (Optional[str]): Config ID.
            chat_group_id (Optional[str]): Chat group ID.
            on_open (Optional[OpenCloseHandlerType]): Handler for when the connection is opened.
            on_message (Optional[MessageHandlerType]): Handler for when a message is received.
            on_error (Optional[ErrorHandlerType]): Handler for when an error occurs.
            on_close (Optional[OpenCloseHandlerType]): Handler for when the connection is closed.
            interruptible (bool): Whether to enable interruptibility.
        """
        uri = self._build_uri(config_id, resumed_chat_group_id)
        logger.info("Connecting to EVI API at %s", uri)

        try:
            async with websockets.connect(
                uri,
                extra_headers=self._get_client_headers(),
                close_timeout=self._close_timeout,
                open_timeout=self._open_timeout,
                max_size=self.DEFAULT_MAX_PAYLOAD_SIZE_BYTES,
            ) as protocol:
                await self._handle_open_close(on_open)

                voice_socket = VoiceSocket(protocol)
                byte_strs: Stream = Stream.new()

                recv_task = asyncio.create_task(
                    self._handle_messages(voice_socket, byte_strs, on_message, interruptible, on_error)
                )
                self._audio_task = asyncio.create_task(self._audio_playback(byte_strs))

                yield voice_socket

                await asyncio.gather(recv_task, self._audio_task)

        except websockets.exceptions.InvalidStatusCode as exc:
            await self._handle_error(exc, on_error)
            if exc.status_code == 401:  # Unauthorized
                raise HumeClientException("HumeVoiceClient initialized with invalid API key.") from exc
            raise HumeClientException("Unexpected error when creating EVI API connection") from exc
        except Exception as exc:
            await self._handle_error(exc, on_error)
            raise
        finally:
            if self._audio_task is not None:
                self._audio_task.cancel()
                try:
                    await self._audio_task
                except asyncio.CancelledError:
                    pass
            await self._handle_open_close(on_close)

    def _build_uri(self, config_id: Optional[str], chat_group_id: Optional[str]) -> str:
        uri_base = self._build_endpoint("evi", "chat", Protocol.WS)
        if config_id and chat_group_id:
            raise HumeClientException(
                "If resuming from a chat_group_id you must not provide a config_id. "
                "The original config for the chat group will be used automatically."
            )
        params: Dict[str, Any] = {}
        if config_id:
            params["config_id"] = config_id
        if chat_group_id:
            params["resumed_chat_group_id"] = chat_group_id
        encoded_params = urllib.parse.urlencode(params)
        return f"{uri_base}?{encoded_params}"
