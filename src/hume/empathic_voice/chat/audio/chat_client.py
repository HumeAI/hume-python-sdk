"""Async client for handling messages to and from an EVI connection."""

import asyncio
import logging
from dataclasses import dataclass

from hume.empathic_voice.chat.audio.asyncio_utilities import Stream
from hume.empathic_voice.chat.audio.audio_utilities import play_audio
from hume.empathic_voice.chat.audio.microphone_sender import Sender
from hume.empathic_voice.chat.socket_client import ChatWebsocketConnection

logger = logging.getLogger(__name__)

@dataclass
class ChatClient:
    """Async client for handling messages to and from an EVI connection."""

    sender: Sender
    byte_strs: Stream[bytes]

    @classmethod
    def new(cls, *, sender: Sender, byte_strs: Stream[bytes]) -> "ChatClient":
        """Create a new chat client.

        Args:
            sender (_Sender): Sender for audio data.
            byte_strs (Stream[bytes]): Byte stream of audio data. 
        """
        return cls(sender=sender, byte_strs=byte_strs)

    async def _play(self) -> None:
        async for byte_str in self.byte_strs:
            await self.sender.on_audio_begin()
            await play_audio(byte_str)
            await self.sender.on_audio_end()

    async def run(self, *, socket: ChatWebsocketConnection) -> None:
        """Run the chat client.

        Args:
            socket (ChatWebsocketConnection): EVI socket.
        """
        send = self.sender.send(socket=socket)

        await asyncio.gather(self._play(), send)