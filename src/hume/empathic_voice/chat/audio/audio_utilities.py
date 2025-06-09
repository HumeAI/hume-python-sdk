# THIS FILE IS MANUALLY MAINTAINED: see .fernignore
"""Utilities for audio playback."""

import asyncio
import io
from typing import TYPE_CHECKING, Optional
from exceptiongroup import ExceptionGroup
import wave # from python stdlib
import queue
import threading

from hume.core.api_error import ApiError

_import_error: Optional[ModuleNotFoundError] = None
try:
    import sounddevice as sd # type: ignore
except ModuleNotFoundError as e:
    _import_error = e

if TYPE_CHECKING:
    import sounddevice as sd # type: ignore


async def play_audio(byte_str: bytes) -> None:
    """Play audio from WAV bytes asynchronously."""
    if _import_error:
        raise ExceptionGroup('Run `pip install "hume[microphone]"` to install dependencies required to use audio playback.', [_import_error])
    
    # Parse WAV header from bytes
    with wave.open(io.BytesIO(byte_str), 'rb') as wav_file:
        sample_rate = wav_file.getframerate()
        channels = wav_file.getnchannels()
        sample_width = wav_file.getsampwidth()
        audio_data = wav_file.readframes(wav_file.getnframes())

    loop = asyncio.get_running_loop()
    
    # Create an asyncio Event to signal completion
    finished_event = asyncio.Event()
    
    # Global state for callback
    data_pos = 0
    
    def callback(outdata, frames, time, status):
        nonlocal data_pos
        if status:
            print(f'Audio status: {status}')
        
        # Calculate how many bytes we need
        bytes_needed = frames * channels * sample_width
        bytes_remaining = len(audio_data) - data_pos
        
        if bytes_remaining <= 0:
            raise sd.CallbackStop
        
        # Copy available data
        bytes_to_copy = min(bytes_needed, bytes_remaining)
        outdata[:bytes_to_copy] = audio_data[data_pos:data_pos + bytes_to_copy]
        
        # Pad with silence if needed
        if bytes_to_copy < bytes_needed:
            outdata[bytes_to_copy:bytes_needed] = b'\x00' * (bytes_needed - bytes_to_copy)
            raise sd.CallbackStop
        
        data_pos += bytes_to_copy
    
    def finished_callback():
        # This runs in the audio thread, so we need to call set() thread-safely
        loop.call_soon_threadsafe(finished_event.set)
    
    try:
        # Start playback
        stream = sd.RawOutputStream(
            samplerate=sample_rate,
            channels=channels,
            dtype=f'int{sample_width * 8}',
            callback=callback,
            finished_callback=finished_callback
        )
        
        with stream:
            # Wait for playback to finish
            await finished_event.wait()
            
    except Exception as e:
        raise RuntimeError(f"Audio playback error: {e}")
