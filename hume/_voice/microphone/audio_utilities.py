"""Utilities for audio playback."""

import asyncio
from io import BytesIO
from typing import Optional

import simpleaudio as sa
from pydub import AudioSegment

# NOTE:
# - expects that byte_str is a valid audio file with the appropriate headers
# - explicitly uses simpleaudio for audio playback


class AudioPlayer:
    def __init__(self) -> None:
        self._playback_object: Optional[sa.PlayObject] = None
        self._stop_event = asyncio.Event()

    async def play_audio(self, byte_str: bytes) -> None:
        """Play a byte string of audio data with the system audio output device.

        Args:
            byte_str (bytes): Byte string of audio data.
        """
        self._stop_event.clear()  # Reset the stop event

        segment = AudioSegment.from_file(BytesIO(byte_str))
        audio_data = segment.raw_data
        num_channels = segment.channels
        bytes_per_sample = segment.sample_width
        sample_rate = segment.frame_rate

        def _play_audio_segment() -> None:
            wave_obj = sa.WaveObject(audio_data, num_channels, bytes_per_sample, sample_rate)
            self._playback_object = wave_obj.play()

        await asyncio.to_thread(_play_audio_segment)

    def stop_audio(self) -> None:
        """Stop the current audio playback."""
        self._stop_event.set()  # Set the stop event to signal stopping

        if self._playback_object:
            self._playback_object.stop()
            self._playback_object = None
