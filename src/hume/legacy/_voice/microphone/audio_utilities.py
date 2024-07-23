"""Utilities for audio playback."""

import asyncio
from io import BytesIO
from hume.legacy.error.hume_client_exception import HumeClientException

try:
    import pydub.playback
    from pydub import AudioSegment
    HAS_AUDIO_DEPENDENCIES = True
except ModuleNotFoundError:
    HAS_AUDIO_DEPENDENCIES = False


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
    if not HAS_AUDIO_DEPENDENCIES:
        raise HumeClientException(
            'Run `pip install "hume[legacy]"` to install dependencies required to use audio playback.'
        )
    segment = AudioSegment.from_file(BytesIO(byte_str))
    await asyncio.to_thread(pydub.playback.play, segment)
