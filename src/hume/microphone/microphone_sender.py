"""Sender for streaming audio from a microphone."""

import json
import logging
from dataclasses import dataclass
from typing import Protocol

from .microphone import Microphone
from ..empathic_voice.chat.socket_client import AsyncChatWSSConnection

logger = logging.getLogger(__name__)


class Sender(Protocol):
    """Protocol for sending streaming audio to an EVI connection."""

    async def on_audio_begin(self) -> None:
        """Handle the start of an audio stream."""
        raise NotImplementedError()

    async def on_audio_end(self) -> None:
        """Handle the end of an audio stream."""
        raise NotImplementedError()

    async def send(self, *, socket: AsyncChatWSSConnection) -> None:
        """Send audio data over an EVI socket.

        Args:
            socket (AsyncChatWSSConnection): EVI socket.
        """
        raise NotImplementedError()

    async def send_tool_response(self, *, socket: AsyncChatWSSConnection, tool_call_id: str, content: str) -> None:
        """Send a tool response over an EVI socket.

        Args:
            socket (AsyncChatWSSConnection): EVI socket.
            tool_call_id (str): Tool call ID.
            content (str): Tool response content.
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

    async def send(self, *, socket: AsyncChatWSSConnection) -> None:
        """Send audio data over an EVI socket.

        Args:
            socket (AsyncChatWSSConnection): EVI socket.
        """
        async for byte_str in self.microphone:
            if self.send_audio:
                await socket._send(byte_str)

    async def send_tool_response(self, *, socket: AsyncChatWSSConnection, tool_call_id: str, content: str) -> None:
        """Send a tool response over an EVI socket.

        Args:
            socket (AsyncChatWSSConnection): EVI socket.
            tool_call_id (str): Tool call ID.
            content (str): Tool response content.
        """
        response_message = {
            "type": "tool_response",
            "tool_call_id": tool_call_id,
            "content": content,
        }
        await socket._send(json.dumps(response_message).encode("utf-8"))
