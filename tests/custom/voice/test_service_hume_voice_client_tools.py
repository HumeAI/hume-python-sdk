import json
import logging
from uuid import uuid4

import pytest

from hume import HumeVoiceClient, LanguageModelConfig, VoiceConfig, VoiceIdentityConfig, VoiceTool
from hume.error.hume_client_exception import HumeClientException

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
        # NOTE: This UUID can be removed when the API supports duplicate config names after deletion.
        name_uuid = str(uuid4())
        tool_name = f"weather-{name_uuid}"
        parameters = json.dumps(WEATHER_TOOL_PARAMETERS)
        new_tool: VoiceTool = voice_client.create_tool(
            name=tool_name,
            parameters=parameters,
        )
        self.check_tool_fields(new_tool, tool_name, parameters)

        config_name = f"weather-assistant-{name_uuid}"
        new_config: VoiceConfig = voice_client.create_config(
            name=config_name,
            prompt=WHETHER_ASSISTANT_PROMPT,
            tools=[new_tool],
            language_model=LanguageModelConfig(model_provider="OPEN_AI", model_resource="gpt-3.5-turbo"),
            voice_identity_config=VoiceIdentityConfig(name="ITO"),
        )

        fetched_tool = voice_client.get_tool(new_tool.id)
        self.check_tool_fields(fetched_tool, tool_name, parameters)

        listed_tools = list(voice_client.iter_tools())
        n_tools = len(listed_tools)
        assert n_tools >= 1

        voice_client.delete_config(new_config.id)
        voice_client.delete_tool(new_tool.id)

        listed_tools = list(voice_client.iter_tools())
        assert len(listed_tools) == n_tools - 1

        match = f"Tool not found with ID: {self.UUID_REGEX}"
        with pytest.raises(HumeClientException, match=match):
            voice_client.get_tool(new_tool.id)

    def check_tool_fields(self, tool: VoiceTool, name: str, parameters: str) -> None:
        assert tool.name == name
        assert tool.parameters == parameters
