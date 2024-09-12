from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import ClassVar

from hume.empathic_voice.chat.audio.microphone import Microphone
from hume.empathic_voice.chat.audio.microphone_sender import MicrophoneSender
from hume.empathic_voice.chat.socket_client import ChatWebsocketConnection
from hume.empathic_voice.chat.audio.chat_client import ChatClient
from hume.empathic_voice.types import AudioConfiguration, SessionSettings
from hume.empathic_voice.chat.audio.asyncio_utilities import Stream

logger = logging.getLogger(__name__)

@dataclass
class MicrophoneInterface:
    """Interface for connecting a device microphone and user-defined audio stream to an EVI connection."""

    DEFAULT_ALLOW_USER_INTERRUPT: ClassVar[bool] = False

    @classmethod
    async def start(
        cls,
        socket: ChatWebsocketConnection,
        byte_stream: Stream[bytes],
        device: int | None = Microphone.DEFAULT_DEVICE,
        allow_user_interrupt: bool = DEFAULT_ALLOW_USER_INTERRUPT,
    ) -> None:
        """Start the microphone interface.

        Args:
            socket (AsyncChatWSSConnection): EVI socket.
            device (int | None): Device index for the microphone.
            allow_user_interrupt (bool): Whether to allow the user to interrupt EVI. If False, the user's microphone input is stopped from flowing to the WebSocket when audio from the assistant is playing.
            byte_stream (Stream[bytes]): Byte stream of audio data.
        """
        with Microphone.context(device=device) as microphone:
            sender = MicrophoneSender.new(microphone=microphone, allow_interrupt=allow_user_interrupt)
            chat_client = ChatClient.new(sender=sender, byte_strs=byte_stream)
            print("Configuring socket with microphone settings...")
            audio_config = AudioConfiguration(sample_rate=microphone.sample_rate,
                                              channels=microphone.num_channels,
                                              encoding="linear16")
            session_settings_config = SessionSettings(audio=audio_config)
            await socket.send_session_settings(
                message=session_settings_config
            )
            print("Microphone connected. Say something!")
            await chat_client.run(socket=socket)