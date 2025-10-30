# THIS FILE IS MANUALLY MAINTAINED: see .fernignore
"""Async client for handling messages to and from an EVI connection."""

import asyncio
import logging
from dataclasses import dataclass
from typing import AsyncIterable

from hume.empathic_voice.chat.audio.audio_utilities import play_audio_streaming
from hume.empathic_voice.chat.audio.microphone_sender import Sender
from hume.empathic_voice.chat.client import AsyncChatSocketClient

logger = logging.getLogger(__name__)

@dataclass
class ChatClient:
    """Async client for handling messages to and from an EVI connection."""

    sender: Sender
    byte_strs: AsyncIterable[bytes]

    @classmethod
    def new(cls, *, sender: Sender, byte_strs: AsyncIterable[bytes]) -> "ChatClient":
        """Create a new chat client.

        Args:
            sender (_Sender): Sender for audio data.
            byte_strs (Stream[bytes]): Byte stream of audio data. 
        """
        return cls(sender=sender, byte_strs=byte_strs)

    async def _play(self) -> None:
        async def iterable() -> AsyncIterable[bytes]:
            first = True
            async for byte_str in self.byte_strs:
                # Each chunk of audio data sent from evi is a .wav
                # file. We want to concatenate these as one long .wav
                # stream rather than playing each individual .wav file
                # and starting and stopping the audio player for each
                # chunk.
                # 
                # Every .wav file starts with a 44 byte header that
                # declares metadata like the sample rate and the number
                # of channels. We assume that the first .wav header
                # applies for the entire stream, so for all but the
                # first chunk we skip the first 44 bytes.
                if not first:
                    byte_str = byte_str[44:]
                yield byte_str
                first = False
        await play_audio_streaming(
            iterable(),
            on_playback_active=self.sender.on_audio_begin,
            on_playback_idle=self.sender.on_audio_end
        )

    async def run(self, *, socket: AsyncChatSocketClient) -> None:
        """Run the chat client.

        Args:
            socket (AsyncChatSocketClient): EVI socket.
        """
        send = self.sender.send(socket=socket)

        await asyncio.gather(self._play(), send)
