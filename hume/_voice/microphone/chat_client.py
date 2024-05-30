"""Async client for handling messages to and from an EVI connection."""

import asyncio
import base64
import datetime
import json
import logging
from dataclasses import dataclass
from typing import ClassVar

from hume._voice.microphone.asyncio_utilities import Stream
from hume._voice.microphone.audio_utilities import play_audio
from hume._voice.microphone.microphone_sender import Sender
from hume._voice.voice_socket import VoiceSocket
from hume.error.hume_client_exception import HumeClientException

logger = logging.getLogger(__name__)


@dataclass
class ChatClient:
    """Async client for handling messages to and from an EVI connection."""

    DEFAULT_USER_ROLE_NAME: ClassVar[str] = "You"
    DEFAULT_ASSISTANT_ROLE_NAME: ClassVar[str] = "EVI"

    sender: Sender
    byte_strs: Stream[bytes]

    @classmethod
    def new(cls, *, sender: Sender) -> "ChatClient":
        """Create a new chat client.

        Args:
            sender (Sender): Sender for audio data.
        """
        return cls(sender=sender, byte_strs=Stream.new())

    @classmethod
    def _map_role(cls, role: str) -> str:
        if role == "user":
            return cls.DEFAULT_USER_ROLE_NAME
        if role == "assistant":
            return cls.DEFAULT_ASSISTANT_ROLE_NAME
        return role

    def _print_prompt(self, text: str) -> None:
        now = datetime.datetime.now(tz=datetime.timezone.utc)
        now_str = now.strftime("%H:%M:%S")
        print(f"[{now_str}] {text}")

    async def _recv(self, *, socket: VoiceSocket) -> None:
        async for socket_message in socket:
            message = json.loads(socket_message)
            if message["type"] in ["user_message", "assistant_message"]:
                role = self._map_role(message["message"]["role"])
                message_text = message["message"]["content"]
                text = f"{role}: {message_text}"
            elif message["type"] == "audio_output":
                message_str: str = message["data"]
                message_bytes = base64.b64decode(message_str.encode("utf-8"))
                await self.byte_strs.put(message_bytes)
                continue
            elif message["type"] == "error":
                error_message: str = message["message"]
                error_code: str = message["code"]
                raise HumeClientException(f"Error ({error_code}): {error_message}")
            elif message["type"] == "tool_call":
                print(
                    "Warning: EVI is trying to make a tool call. "
                    "Either remove tool calling from your config or "
                    "use the VoiceSocket directly without a MicrophoneInterface."
                )
                tool_call_id = message["tool_call_id"]
                if message["response_required"]:
                    content = "Let's start over"
                    await self.sender.send_tool_response(socket=socket, tool_call_id=tool_call_id, content=content)
                continue
            elif message["type"] == "chat_metadata":
                message_type = message["type"].upper()
                chat_id = message["chat_id"]
                chat_group_id = message["chat_group_id"]
                text = f"<{message_type}> Chat ID: {chat_id}, Chat Group ID: {chat_group_id}"
            else:
                message_type = message["type"].upper()
                text = f"<{message_type}>"

            self._print_prompt(text)

    async def _play(self) -> None:
        async for byte_str in self.byte_strs:
            await self.sender.on_audio_begin()
            await play_audio(byte_str)
            await self.sender.on_audio_end()

    async def run(self, *, socket: VoiceSocket) -> None:
        """Run the chat client.

        Args:
            socket (VoiceSocket): EVI socket.
        """
        recv = self._recv(socket=socket)
        send = self.sender.send(socket=socket)

        await asyncio.gather(recv, self._play(), send)
