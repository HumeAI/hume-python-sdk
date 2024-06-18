"""Utility class for audio playback."""

import asyncio
from io import BytesIO

import pydub.playback
from pydub import AudioSegment

# NOTE:
# - expects that byte_str is a valid audio file with the appropriate headers
# - implicitly relies on simpleaudio OR pyaudio OR ffmpeg, defaulting in that order.
#   - [https://stackoverflow.com/a/20746883]
#   - [https://github.com/jiaaro/pydub#playback]
#   - [https://github.com/jiaaro/pydub/blob/master/pydub/playback.py]
# - stop_audio() allows for the decoupling of interruptibility from the MicrophoneSender class.


class AudioPlayer:
    def __init__(self) -> None:
        self._playback_object = None
        self._stop_event = asyncio.Event()

    async def play_audio(self, byte_str: bytes) -> None:
        """Play a byte string of audio data with the system audio output device.

        Args:
            byte_str (bytes): Byte string of audio data.
        """
        self._stop_event.clear()  # Reset the stop event

        segment = AudioSegment.from_file(BytesIO(byte_str))

        def _play_audio_segment() -> None:
            self._playback_object = pydub.playback.play(segment)

        await asyncio.to_thread(_play_audio_segment)

    def stop_audio(self) -> None:
        """Stop the current audio playback."""
        self._stop_event.set()  # Set the stop event to signal stopping

        if self._playback_object:
            self._playback_object.stop()
            self._playback_object = None
