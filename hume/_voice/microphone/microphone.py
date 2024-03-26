import asyncio
import contextlib
import dataclasses
from typing import AsyncIterator, ClassVar, Iterator, Optional

import _cffi_backend as cffi_backend
import sounddevice
from _cffi_backend import _CDataBase as CDataBase  # pylint: disable=no-name-in-module
from sounddevice import CallbackFlags, RawInputStream

from hume._voice.microphone.asyncio_utilities import Stream


@dataclasses.dataclass
class Microphone:
    # NOTE: use int16 for compatibility with deepgram
    DATA_TYPE: ClassVar[str] = "int16"
    DEFAULT_DEVICE: ClassVar[Optional[int]] = None

    stream: Stream[bytes]
    num_channels: int
    sample_rate: int

    # NOTE: implementation based on
    # [https://python-sounddevice.readthedocs.io/en/0.4.6/examples.html#creating-an-asyncio-generator-for-audio-blocks]
    @classmethod
    @contextlib.contextmanager
    def context(cls, *, device: Optional[int] = DEFAULT_DEVICE) -> Iterator["Microphone"]:
        if device is None:
            device = sounddevice.default.device[0]
        sound_device = sounddevice.query_devices(device=device)

        num_channels = sound_device["max_input_channels"]

        if num_channels == 0:
            devices = sounddevice.query_devices()
            message = (
                "Selected input device does not have any input channels. \n"
                "Please set MicrophoneInterface(device=<YOUR DEVICE ID>). \n"
                f"Devices:\n{devices}"
            )
            raise IOError(message)

        # NOTE: use asyncio.get_running_loop() over asyncio.get_event_loop() per
        # [https://docs.python.org/3/library/asyncio-eventloop.html#asyncio.get_event_loop]
        sample_rate = int(sound_device["default_samplerate"])
        microphone = cls(stream=Stream.new(), num_channels=num_channels, sample_rate=sample_rate)
        event_loop = asyncio.get_running_loop()

        # pylint: disable=c-extension-no-member
        # NOTE:
        # - cffi types determined by logging; see more at [https://cffi.readthedocs.io/en/stable/ref.html]
        # - put_nowait(indata[:]) seems to block, so use call_soon_threadsafe() like the reference implementation
        def callback(indata: cffi_backend.buffer, _frames: int, _time: CDataBase, _status: CallbackFlags) -> None:
            event_loop.call_soon_threadsafe(microphone.stream.queue.put_nowait, indata[:])

        with RawInputStream(callback=callback, dtype=cls.DATA_TYPE):
            yield microphone

    def __aiter__(self) -> AsyncIterator[bytes]:
        return self.stream
