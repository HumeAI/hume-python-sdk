import logging
from dataclasses import dataclass
from typing import Protocol

from hume.empathic_voice.chat.audio.microphone import Microphone
from hume.empathic_voice.chat.socket_client import ChatWebsocketConnection

logger = logging.getLogger(__name__)

class Sender(Protocol):
    """Protocol for sending streaming audio to an EVI connection."""

    async def send(self, *, socket: ChatWebsocketConnection) -> None:
        """Send audio data over an EVI socket.

        Args:
            socket (ChatWebsocketConnection): EVI socket.
        """
        raise NotImplementedError()

@dataclass
class MicrophoneSender(Sender):
    """Sender for streaming audio from a microphone."""

    microphone: Microphone

    @classmethod
    def new(cls, *, microphone: Microphone) -> "MicrophoneSender":
        """Create a new microphone sender.

        Args:
            microphone (Microphone): Microphone instance.
        """
        return cls(microphone=microphone)

    async def send(self, *, socket: ChatWebsocketConnection) -> None:
        """Send audio data over an EVI socket.

        Args:
            socket (ChatWebsocketConnection): EVI socket.
        """
        async for byte_str in self.microphone:
            await socket._send(byte_str)