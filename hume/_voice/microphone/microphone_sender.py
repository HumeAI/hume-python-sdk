"""Sender for streaming audio from a microphone."""

import logging
from dataclasses import dataclass
from typing import Protocol

from hume._voice.microphone.microphone import Microphone
from hume._voice.voice_socket import VoiceSocket

logger = logging.getLogger(__name__)


class Sender(Protocol):
    """Protocol for sending streaming audio to an EVI connection."""

    async def on_audio_begin(self) -> None:
        """Handle the start of an audio stream."""
        raise NotImplementedError()

    async def on_audio_end(self) -> None:
        """Handle the end of an audio stream."""
        raise NotImplementedError()

    async def send(self, *, socket: VoiceSocket) -> None:
        """Send audio data over an EVI socket.

        Args:
            socket (VoiceSocket): EVI socket.
        """
        raise NotImplementedError()


@dataclass
class MicrophoneSender(Sender):
    """Sender for streaming audio from a microphone."""

    microphone: Microphone
    send_audio: bool
    allow_interrupt: bool

    @classmethod
    def new(cls, *, microphone: Microphone, allow_interrupt: bool) -> "MicrophoneSender":
        """Create a new microphone sender.

        Args:
            microphone (Microphone): Microphone instance.
            allow_interrupt (bool): Whether to allow interrupting the audio stream.
        """
        return cls(microphone=microphone, send_audio=True, allow_interrupt=allow_interrupt)

    async def on_audio_begin(self) -> None:
        """Handle the start of an audio stream."""
        self.send_audio = self.allow_interrupt

    async def on_audio_end(self) -> None:
        """Handle the end of an audio stream."""
        self.send_audio = True

    async def send(self, *, socket: VoiceSocket) -> None:
        """Send audio data over an EVI socket.

        Args:
            socket (VoiceSocket): EVI socket.
        """
        async for byte_str in self.microphone:
            if self.send_audio:
                await socket.send(byte_str)
