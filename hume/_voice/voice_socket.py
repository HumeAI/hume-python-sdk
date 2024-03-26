"""Voice socket connection."""

from pathlib import Path
from typing import Any, AsyncIterator, ClassVar

from pydub import AudioSegment
from websockets.client import WebSocketClientProtocol as WebSocket


class VoiceSocket:
    """Voice socket connection."""

    N_CHANNELS: ClassVar[int] = 1
    SAMPLE_RATE: ClassVar[int] = 16_000

    def __init__(self, protocol: WebSocket):
        """Construct a `VoiceSocket`.

        Args:
            protocol (WebSocketClientProtocol): Protocol instance from websockets library.

        Raises:
            HumeClientException: If there is an error processing media over the socket connection.
        """
        self._protocol = protocol

    async def __aiter__(self) -> AsyncIterator[Any]:
        async for message in self._protocol:
            yield message

    async def send(self, byte_str: bytes) -> None:
        await self._protocol.send(byte_str)

    async def recv(self) -> Any:
        await self._protocol.recv()

    async def send_file(self, filepath: Path) -> None:
        with filepath.open("rb") as f:
            segment: AudioSegment = AudioSegment.from_wav(f)
            segment = segment.set_frame_rate(self.SAMPLE_RATE).set_channels(self.N_CHANNELS)
            audio_bytes = segment.raw_data
            await self._protocol.send(audio_bytes)
