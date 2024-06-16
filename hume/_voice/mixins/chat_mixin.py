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
from hume._voice.microphone.audio_utilities import play_audio, stop_audio
from hume._voice.voice_socket import VoiceSocket
from hume.error.hume_client_exception import HumeClientException

logger = logging.getLogger(__name__)

OpenCloseHandlerType = Union[Callable[[], None], Callable[[], Awaitable[None]]]
MessageHandlerType = Union[Callable[[dict], None], Callable[[dict], Awaitable[None]]]
ErrorHandlerType = Union[Callable[[Exception], None], Callable[[Exception], Awaitable[None]]]


class ChatMixin(ClientBase):
    """Client operations for EVI WebSocket connections."""

    DEFAULT_MAX_PAYLOAD_SIZE_BYTES: ClassVar[int] = 2**24

    @asynccontextmanager
    async def connect(
        self,
        config_id: Optional[str] = None,
        chat_group_id: Optional[str] = None,
        on_open: Optional[OpenCloseHandlerType] = None,
        on_close: Optional[OpenCloseHandlerType] = None,
        on_error: Optional[ErrorHandlerType] = None,
        on_message: Optional[MessageHandlerType] = None,
        interruptible: bool = False,
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
        uri_base = self._build_endpoint("evi", "chat", Protocol.WS)

        if config_id is not None and chat_group_id is not None:
            raise HumeClientException(
                "If resuming from a chat_group_id you must not provide a config_id. "
                "The original config for the chat group will be used automatically."
            )

        params: Dict[str, Any] = {}
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
                if on_open is not None:
                    if asyncio.iscoroutinefunction(on_open):
                        await on_open()
                    else:
                        on_open()

                voice_socket = VoiceSocket(protocol)
                byte_strs: Stream = Stream.new()

                async def handle_messages() -> None:
                    try:
                        async for socket_message in voice_socket:
                            # Ensure the message is parsed as JSON
                            message = json.loads(socket_message)

                            if on_message is not None:
                                if asyncio.iscoroutinefunction(on_message):
                                    await on_message(message)
                                else:
                                    on_message(message)

                            if message["type"] == "audio_output":
                                message_str: str = message["data"]
                                message_bytes = base64.b64decode(message_str.encode("utf-8"))
                                await byte_strs.put(message_bytes)
                                continue  # Skip calling the on_message handler for audio_output

                            if interruptible and message["type"] == "user_interruption":
                                logger.debug("Received user_interruption message")
                                await stop_audio()
                    except Exception as exc:
                        if on_error:
                            if asyncio.iscoroutinefunction(on_error):
                                await on_error(exc)
                            else:
                                on_error(exc)
                        raise

                async def audio_playback() -> None:
                    async for byte_str in byte_strs:
                        await play_audio(byte_str)

                """
                Originally in ChatClient, the audio_playback() method was the following:

                    async for byte_str in byte_strs:
                        await sender.on_audio_begin()
                        await play_audio(byte_str)
                        await sender.on_audio_end()
                
                This allowed the user, when initializing the MicrophoneInterface,
                to choose if their MicrophoneSender allowed interruptibility or not.
                
                With these changes, interruptibility is entirely decoupled from the microphone.
                """

                recv_task = asyncio.create_task(handle_messages())
                audio_task = asyncio.create_task(audio_playback())

                yield voice_socket

                await asyncio.gather(recv_task, audio_task)

        except websockets.exceptions.InvalidStatusCode as exc:
            if on_error is not None:
                if asyncio.iscoroutinefunction(on_error):
                    await on_error(exc)
                else:
                    on_error(exc)
            status_code: int = exc.status_code
            if status_code == 401:  # Unauthorized
                message = "HumeVoiceClient initialized with invalid API key."
                raise HumeClientException(message) from exc
            raise HumeClientException("Unexpected error when creating EVI API connection") from exc
        except Exception as exc:
            if on_error is not None:
                if asyncio.iscoroutinefunction(on_error):
                    await on_error(exc)
                else:
                    on_error(exc)
            raise
        finally:
            if on_close is not None:
                if asyncio.iscoroutinefunction(on_close):
                    await on_close()
                else:
                    on_close()
