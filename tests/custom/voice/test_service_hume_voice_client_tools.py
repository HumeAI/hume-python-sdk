import json
import logging
from uuid import uuid4

import pytest

from hume.client import HumeClient
from hume.empathic_voice.types.return_user_defined_tool import ReturnUserDefinedTool

logger = logging.getLogger(__name__)


WEATHER_TOOL_PARAMETERS = {
    "type": "object",
    "properties": {
        "location": {
            "type": "string",
            "description": "The city and state, e.g. San Francisco, CA",
        },
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

    def test_tool_operations(self, hume_client: HumeClient) -> None:
        # NOTE: This UUID can be removed when the API supports duplicate config names after deletion.
        name_uuid = str(uuid4())
        tool_name = f"weather-{name_uuid}"
        parameters = json.dumps(WEATHER_TOOL_PARAMETERS)
        new_tool = hume_client.empathic_voice.tools.create_tool(
            name=tool_name,
            parameters=parameters,
        )
        self.check_tool_fields(new_tool, tool_name, parameters) # type: ignore

        listed_tools = list(hume_client.empathic_voice.tools.list_tools())
        n_tools = len(listed_tools)
        assert n_tools >= 1

        hume_client.empathic_voice.tools.delete_tool(new_tool.id) # type: ignore

        listed_tools = list(hume_client.empathic_voice.tools.list_tools())
        assert len(listed_tools) == n_tools - 1

    def check_tool_fields(
        self, tool: ReturnUserDefinedTool, name: str, parameters: str
    ) -> None:
        assert tool.name == name
        assert tool.parameters == parameters
