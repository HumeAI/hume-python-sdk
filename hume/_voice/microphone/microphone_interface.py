import asyncio
import datetime
import json
import logging
from dataclasses import dataclass
from typing import ClassVar, Optional, Protocol

from hume._voice.microphone.asyncio_utilities import Stream
from hume._voice.microphone.audio_utilities import play_audio
from hume._voice.microphone.microphone import Microphone
from hume._voice.voice_socket import VoiceSocket

logger = logging.getLogger(__name__)


class Sender(Protocol):
    async def on_audio_begin(self) -> None:
        raise NotImplementedError()

    async def on_audio_end(self) -> None:
        raise NotImplementedError()

    async def send(self, *, socket: VoiceSocket) -> None:
        raise NotImplementedError()


@dataclass
class MicrophoneSender(Sender):
    microphone: Microphone
    send_audio: bool
    allow_interrupt: bool

    @classmethod
    def new(cls, *, microphone: Microphone, allow_interrupt: bool) -> "MicrophoneSender":
        return cls(microphone=microphone, send_audio=True, allow_interrupt=allow_interrupt)

    async def on_audio_begin(self) -> None:
        self.send_audio = self.allow_interrupt

    async def on_audio_end(self) -> None:
        self.send_audio = True

    async def send(self, *, socket: VoiceSocket) -> None:
        async for byte_str in self.microphone:
            if self.send_audio:
                await socket.send(byte_str)


@dataclass
class ChatClient:
    DEFAULT_USER_ROLE_NAME: ClassVar[str] = "You"
    DEFAULT_ASSISTANT_ROLE_NAME: ClassVar[str] = "EVI"

    sender: Sender
    byte_strs: Stream[bytes]

    @classmethod
    def new(cls, *, sender: Sender) -> "ChatClient":
        return cls(sender=sender, byte_strs=Stream.new())

    @classmethod
    def map_role(cls, role: str) -> str:
        if role == "user":
            return cls.DEFAULT_USER_ROLE_NAME
        elif role == "assistant":
            return cls.DEFAULT_ASSISTANT_ROLE_NAME
        return role

    async def _recv(self, *, socket: VoiceSocket) -> None:
        async for message in socket:
            if isinstance(message, bytes):
                await self.byte_strs.put(message)
            elif isinstance(message, str):
                obj = json.loads(message)
                if obj["type"] in ["user_message", "assistant_message"]:
                    role = self.map_role(obj["message"]["role"])
                    message_text = obj["message"]["content"]
                    text = f"{role}: {message_text}"
                else:
                    message_type = obj["type"].upper()
                    text = f"<{message_type}>"

                now = datetime.datetime.now(tz=datetime.timezone.utc)
                now_str = now.strftime("%H:%M:%S")

                print(f"[{now_str}] {text}")
            else:
                raise ValueError(f"invalid result: {message}")

    async def _play(self) -> None:
        async for byte_str in self.byte_strs:
            await self.sender.on_audio_begin()
            await play_audio(byte_str)
            await self.sender.on_audio_end()

    async def run(self, *, socket: VoiceSocket) -> None:
        recv = self._recv(socket=socket)
        send = self.sender.send(socket=socket)

        await asyncio.gather(recv, self._play(), send)


@dataclass
class MicrophoneInterface:

    @classmethod
    async def start(
        cls,
        socket: VoiceSocket,
        device: Optional[int] = Microphone.DEFAULT_DEVICE,
    ) -> None:
        with Microphone.context(device=device) as microphone:
            sender = MicrophoneSender.new(microphone=microphone, allow_interrupt=True)
            chat_client = ChatClient.new(sender=sender)
            print("Microphone connected. Say something!")
            await chat_client.run(socket=socket)
