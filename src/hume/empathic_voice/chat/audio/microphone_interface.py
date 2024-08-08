from __future__ import annotations

import logging
from dataclasses import dataclass

from hume.empathic_voice.chat.audio.microphone import Microphone
from hume.empathic_voice.chat.audio.microphone_sender import MicrophoneSender
from hume.empathic_voice.chat.socket_client import ChatWebsocketConnection
from hume.empathic_voice.types import AudioConfiguration, SessionSettings

logger = logging.getLogger(__name__)

@dataclass
class MicrophoneInterface:
    """Interface for connecting a device microphone to an EVI connection."""

    @classmethod
    async def start(
        cls,
        socket: ChatWebsocketConnection,
        device: int | None = Microphone.DEFAULT_DEVICE
    ) -> None:
        """Start the microphone interface.

        Args:
            socket (AsyncChatWSSConnection): EVI socket.
            device (int | None): Device index for the microphone.
        """
        with Microphone.context(device=device) as microphone:
            sender = MicrophoneSender.new(microphone=microphone)
            print("Configuring socket with microphone settings...")
            audio_config = AudioConfiguration(sample_rate=microphone.sample_rate,
                                              channels=microphone.num_channels,
                                              encoding="linear16")
            session_settings_config = SessionSettings(audio=audio_config)
            await socket.send_session_settings(
                message=session_settings_config
            )
            print("Microphone connected. Say something!")
            await sender.send(socket=socket)