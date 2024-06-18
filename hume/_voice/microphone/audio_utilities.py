"""Utilities for audio playback."""

import asyncio
from io import BytesIO

import pydub.playback
from pydub import AudioSegment

playback_object = None
stop_event = asyncio.Event()

# NOTE:
# - expects that byte_str is a valid audio file with the appropriate headers
# - implicitly relies on simpleaudio OR pyaudio OR ffmpeg, defaulting in that order.
#   - [https://stackoverflow.com/a/20746883]
#   - [https://github.com/jiaaro/pydub#playback]
#   - [https://github.com/jiaaro/pydub/blob/master/pydub/playback.py]
# - stop_audio() allows for the decoupling of interruptibility from the MicrophoneSender class.


async def play_audio(byte_str: bytes) -> None:
    """Play a byte string of audio data with the system audio output device.

    Args:
        byte_str (bytes): Byte string of audio data.
    """
    global playback_object, stop_event

    stop_event.clear()  # Reset the stop event

    segment = AudioSegment.from_file(BytesIO(byte_str))

    def _play_audio_segment() -> None:
        global playback_object
        playback_object = pydub.playback.play(segment)

    await asyncio.to_thread(_play_audio_segment)


async def stop_audio() -> None:
    """Stop the current audio playback."""
    global playback_object, stop_event
    stop_event.set()  # Set the stop event to signal stopping

    if playback_object and playback_object.is_playing():
        playback_object.stop()
