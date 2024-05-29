import json
import logging
from typing import Tuple
from urllib.request import urlretrieve
from uuid import uuid4

import pytest

from hume import HumeVoiceClient
from hume._voice.models.configs_models import LanguageModelConfig, VoiceConfig, VoiceIdentityConfig
from hume._voice.models.tools_models import VoiceTool
from utilities.eval_data import EvalData

logger = logging.getLogger(__name__)


@pytest.fixture(name="voice_client", scope="module")
def voice_client_fixture(hume_api_key: str) -> HumeVoiceClient:
    return HumeVoiceClient(hume_api_key)


WEATHER_TOOL_PARAMETERS = {
    "type": "object",
    "properties": {
        "location": {"type": "string", "description": "The city and state, e.g. San Francisco, CA"},
        "format": {
            "type": "string",
            "enum": ["celsius", "fahrenheit"],
            "description": "The temperature unit to use. Infer this from the users location.",
        },
    },
    "required": ["location", "format"],
}
WHETHER_ASSISTANT_PROMPT = (
    "You are a helpful assistant who can use tools. "
    "You are having a conversation with the user, who may change their mind. "
    "Follow their instructions obediently. "
    "For example, if the user says 'Never mind' or 'cancel', immediately reply with something deferential."
)


@pytest.mark.asyncio
@pytest.mark.voice
@pytest.mark.service
class TestServiceHumeVoiceClientChat:
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

    def create_weather_tool_config(self, voice_client: HumeVoiceClient) -> Tuple[VoiceConfig, VoiceTool]:
        # NOTE: This UUID can be removed when the API supports duplicate config names after deletion.
        name_uuid = str(uuid4())
        tool_name = f"weather-{name_uuid}"
        parameters = json.dumps(WEATHER_TOOL_PARAMETERS)
        tool: VoiceTool = voice_client.create_tool(
            name=tool_name,
            parameters=parameters,
        )

        config_name = f"weather-assistant-{name_uuid}"
        config: VoiceConfig = voice_client.create_config(
            name=config_name,
            prompt=WHETHER_ASSISTANT_PROMPT,
            tools=[tool],
            language_model=LanguageModelConfig(model_provider="OPEN_AI", model_resource="gpt-3.5-turbo"),
            voice_identity_config=VoiceIdentityConfig(name="ITO"),
        )

        return config, tool

    def clean_up(self, voice_client: HumeVoiceClient, config: VoiceConfig, tool: VoiceTool) -> None:
        voice_client.delete_config(config.id)
        voice_client.delete_tool(tool.id)

    async def test_tool_use(
        self,
        eval_data: EvalData,
        voice_client: HumeVoiceClient,
        tmp_path_factory: pytest.TempPathFactory,
    ) -> None:
        data_url = eval_data["weather-in-la"]
        data_filepath = tmp_path_factory.mktemp("data-dir") / "sample.wav"
        urlretrieve(data_url, data_filepath)

        config, tool = self.create_weather_tool_config(voice_client)

        async with voice_client.connect(config_id=config.id) as socket:
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

        self.clean_up(voice_client, config, tool)
