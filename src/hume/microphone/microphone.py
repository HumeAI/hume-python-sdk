"""Abstraction for handling microphone input."""

import asyncio
import contextlib
import dataclasses
import logging
from typing import AsyncIterator, ClassVar, Iterator, Optional, Any

from .asyncio_utilities import Stream

import sounddevice                                   
from sounddevice import CallbackFlags, RawInputStream, DeviceList

logger = logging.getLogger(__name__)


@dataclasses.dataclass
class Microphone:
    """Abstraction for handling microphone input."""

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
        """Create a new microphone context.

        Args:
            device (Optional[int]): Input device ID.
        """
        sound_device = sounddevice.query_devices(device=device)

        # If you've received a list, then you need to select a device
        # the logic to do so is:
        # 1. Get the list of default devices
        # 2. Check if the default device is in the list of available input devices
        # 3. If it is, select it
        # 4. If it is not, select the first available input device
        if isinstance(sound_device, DeviceList):
            if len(sound_device) == 0:
                message = ("No input devices were found.")
                raise IOError(message)

            # Try to match a default device with the available devices
            default_devices = sounddevice.default.device
            default_input_device = None

            available_device_indeces = [item["index"] for item in sound_device]
            for item in default_devices:
                if item in available_device_indeces:
                    # If there are input channels, let's assume it's an input device
                    default_device = sounddevice.query_devices(device=item)
                    if default_device["max_input_channels"] > 0:
                        default_input_device = sounddevice.query_devices(device=item)
                    break

            # If you cannot match a default device, just select any available one with input channels
            if default_input_device is None:
                for device in sound_device:
                    if device["max_input_channels"] > 0:
                        sound_device = device
                        break
            else:
                sound_device = default_input_device

        if sound_device is None:
            message = ("No input devices were found.")
            raise IOError(message)

        logger.info(f"sound_device: {sound_device}")

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
        def callback(indata: Any, _frames: int, _time: Any, _status: CallbackFlags) -> None:
            event_loop.call_soon_threadsafe(microphone.stream.queue.put_nowait, indata[:])

        with RawInputStream(callback=callback, dtype=cls.DATA_TYPE):
            yield microphone

    def __aiter__(self) -> AsyncIterator[bytes]:
        """Iterate over bytes of microphone input."""
        return self.stream
