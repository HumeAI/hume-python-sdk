"""Interface for connecting a device microphone to an EVI connection."""

import logging
from dataclasses import dataclass
from typing import ClassVar, Optional

from hume._voice.microphone.chat_client import ChatClient
from hume._voice.microphone.microphone import Microphone
from hume._voice.microphone.microphone_sender import MicrophoneSender
from hume._voice.voice_socket import VoiceSocket

logger = logging.getLogger(__name__)


@dataclass
class MicrophoneInterface:
    """Interface for connecting a device microphone to an EVI connection."""

    DEFAULT_ALLOW_USER_INTERRUPT: ClassVar[bool] = False

    @classmethod
    async def start(
        cls,
        socket: VoiceSocket,
        device: Optional[int] = Microphone.DEFAULT_DEVICE,
        allow_user_interrupt: bool = DEFAULT_ALLOW_USER_INTERRUPT,
    ) -> None:
        """Start the microphone interface.

        Args:
            socket (VoiceSocket): EVI socket.
            device (Optional[int]): Device index for the microphone.
            allow_user_interrupt (bool): Whether to allow the user to interrupt EVI.
        """
        with Microphone.context(device=device) as microphone:
            sender = MicrophoneSender.new(microphone=microphone, allow_interrupt=allow_user_interrupt)
            chat_client = ChatClient.new(sender=sender)
            print("Configuring socket with microphone settings...")
            await socket.update_session_settings(
                sample_rate=microphone.sample_rate,
                num_channels=microphone.num_channels,
            )
            print("Microphone connected. Say something!")
            await chat_client.run(socket=socket)
