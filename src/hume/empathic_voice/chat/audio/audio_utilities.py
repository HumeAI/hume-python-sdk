# THIS FILE IS MANUALLY MAINTAINED: see .fernignore
"""Utilities for audio playback."""

import asyncio
from io import BytesIO
from typing import Optional
from exceptiongroup import ExceptionGroup

from hume.core.api_error import ApiError

_import_error: Optional[ModuleNotFoundError] = None
try:
    import pydub.playback
    from pydub import AudioSegment
except ModuleNotFoundError as e:
    _import_error = e




# NOTE:
# - expects that byte_str is a valid audio file with the appropriate headers
# - implicitly relies on simpleaudio:
#   - [https://stackoverflow.com/a/20746883]
#   - [https://github.com/jiaaro/pydub#playback]
#   - [https://github.com/jiaaro/pydub/blob/master/pydub/playback.py]
async def play_audio(byte_str: bytes) -> None:
    """Play a byte string of audio data with the system audio output device.

    Args:
        byte_str (bytes): Byte string of audio data.
    """
    if _import_error:
        raise ExceptionGroup('Run `pip install "hume[microphone]"` to install dependencies required to use audio playback.', [_import_error])
    segment = AudioSegment.from_file(BytesIO(byte_str)) # type: ignore
    await asyncio.to_thread(pydub.playback.play, segment)
