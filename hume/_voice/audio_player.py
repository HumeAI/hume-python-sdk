"""Utilities for audio playback.

This module provides the AudioPlayer class for playing audio byte streams using the system's audio output device.
"""

import asyncio
from io import BytesIO
from typing import Optional

import simpleaudio as sa
from pydub import AudioSegment

# NOTE:
# - expects that byte_str is a valid audio file with the appropriate headers
# - explicitly uses simpleaudio for audio playback


class AudioPlayer:
    """Audio player for playing audio byte streams using the system's audio output device.

    This class uses simpleaudio for audio playback and pydub for handling audio data.
    """

    def __init__(self) -> None:
        """Initialize the AudioPlayer."""
        self._playback_object: Optional[sa.PlayObject] = None
        self._stop_event = asyncio.Event()
        self._play_lock = asyncio.Lock()

    async def play_audio(self, byte_str: bytes) -> None:
        """Play a byte string of audio data with the system audio output device.

        Args:
            byte_str (bytes): Byte string of audio data.
        """
        async with self._play_lock:
            # Wait for any existing playback to complete
            if self._playback_object is not None:
                self._playback_object.wait_done()

            # Reset the stop event for new playback
            self._stop_event.clear()

            # Convert byte string to an AudioSegment
            segment = AudioSegment.from_file(BytesIO(byte_str))
            audio_data = segment.raw_data
            num_channels = segment.channels
            bytes_per_sample = segment.sample_width
            sample_rate = segment.frame_rate

            def _play_audio_segment() -> None:
                """Play the audio segment using simpleaudio."""
                wave_obj = sa.WaveObject(audio_data, num_channels, bytes_per_sample, sample_rate)
                self._playback_object = wave_obj.play()

            # Offload the playback to a separate thread
            await asyncio.to_thread(_play_audio_segment)

    def stop_audio(self) -> None:
        """Stop the current audio playback."""
        # Signal to stop playback
        self._stop_event.set()

        if self._playback_object:
            self._playback_object.stop()
            self._playback_object = None
