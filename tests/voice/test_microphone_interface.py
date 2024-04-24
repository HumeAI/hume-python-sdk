import logging
import re
from unittest.mock import MagicMock

import pytest

from hume import MicrophoneInterface
from hume.error.hume_client_exception import HumeClientException

logger = logging.getLogger(__name__)


@pytest.mark.asyncio
@pytest.mark.voice
class TestMicrophoneInterface:

    async def test_missing_playback_dependencies(self) -> None:
        mock_socket = MagicMock(return_value="mock-socket")
        message = 'Run `pip install "hume[microphone]"` to install dependencies required to use microphone playback.'
        with pytest.raises(HumeClientException, match=re.escape(message)):
            await MicrophoneInterface.start(mock_socket)
