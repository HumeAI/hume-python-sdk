import logging

import pytest

try:
    # pylint: disable=unused-import
    import simpleaudio  # noqa: F401
    import sounddevice  # noqa: F401

    HAS_AUDIO_DEPENDENCIES = True
except ModuleNotFoundError:
    HAS_AUDIO_DEPENDENCIES = False


logger = logging.getLogger(__name__)


@pytest.mark.voice
@pytest.mark.microphone
class TestMicrophone:

    def test_microphone_requirements(self) -> None:
        assert HAS_AUDIO_DEPENDENCIES
