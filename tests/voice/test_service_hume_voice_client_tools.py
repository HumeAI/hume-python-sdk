import json
import logging
from uuid import uuid4

import pytest

from hume import HumeVoiceClient, VoiceTool
from hume._voice.models.configs_models import LanguageModelConfig, VoiceConfig, VoiceIdentityConfig

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


@pytest.mark.voice
@pytest.mark.service
class TestServiceHumeVoiceClientTools:
    UUID_REGEX = r"[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}"

    def test_tool_operations(self, voice_client: HumeVoiceClient) -> None:

        tool_name_uuid = str(uuid4())
        new_tool: VoiceTool = voice_client.create_tool(
            name=f"weather-{tool_name_uuid}",
            parameters=json.dumps(WEATHER_TOOL_PARAMETERS),
        )
        logger.info(f"Created tool: {new_tool.id}")

        config_name_uuid = str(uuid4())
        new_config: VoiceConfig = voice_client.create_config(
            name=f"weather-assistant-{config_name_uuid}",
            prompt=WHETHER_ASSISTANT_PROMPT,
            tools=[new_tool],
            language_model=LanguageModelConfig(model_provider="OPEN_AI", model_resource="gpt-3.5-turbo"),
            voice_identity_config=VoiceIdentityConfig(name="ITO"),
        )
        logger.info(f"Created config: {new_config.id}")

        fetched_tool = voice_client.get_tool(new_tool.id)
        logger.info(f"Fetched tool: {fetched_tool.name}")

        fetched_config = voice_client.get_config(new_config.id)
        logger.info(f"Fetched config: {fetched_config.name}")

        logger.info("Tools")
        for tool in voice_client.iter_tools():
            logger.info(f"- {tool.name} ({tool.id})")

        logger.info("Configs")
        for config in voice_client.iter_configs():
            logger.info(f"- {config.name} ({config.id})")

        voice_client.delete_config(new_config.id)
        voice_client.delete_tool(new_tool.id)
