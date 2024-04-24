import json
import logging
from urllib.request import urlretrieve

import pytest

from hume import HumeVoiceClient
from utilities.eval_data import EvalData

logger = logging.getLogger(__name__)


@pytest.fixture(name="voice_client", scope="module")
def voice_client_fixture(hume_api_key: str) -> HumeVoiceClient:
    return HumeVoiceClient(hume_api_key)


@pytest.mark.asyncio
@pytest.mark.voice
@pytest.mark.service
class TestServiceHumeVoiceClientChat:
    UUID_REGEX = r"[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}"

    async def test_chat(
        self,
        eval_data: EvalData,
        voice_client: HumeVoiceClient,
        tmp_path_factory: pytest.TempPathFactory,
    ) -> None:
        data_url = eval_data["know-any-good-jokes"]
        data_filepath = tmp_path_factory.mktemp("data-dir") / "sample.wav"
        urlretrieve(data_url, data_filepath)

        async with voice_client.connect() as socket:
            await socket.update_session_settings(sample_rate=16_000, num_channels=1)

            await socket.send_file(data_filepath)
            messages = []
            async for message_str in socket:
                logger.info("Received message on socket")
                message = json.loads(message_str)

                assert "type" in message, f"Expected message to have a 'type' field: {message}"

                # Simplify messages for logging
                if message["type"] == "audio_output":
                    message["data"] = "<redacted>"
                if message["type"] in ["user_message", "assistant_message"]:
                    message["models"] = "<redacted>"

                message_str = json.dumps(message, indent=2)
                logger.info(f"Message: {message_str}")

                messages.append(message)

                if message["type"] in ["error", "assistant_end"]:
                    return
