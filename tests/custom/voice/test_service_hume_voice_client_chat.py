import os

import json
import logging
from typing import Tuple
from urllib.request import urlretrieve
from uuid import uuid4

import pytest

from hume.client import HumeClient
from hume.empathic_voice.chat.socket_client import AsyncChatConnectOptions
from hume.empathic_voice.types.audio_configuration import AudioConfiguration
from hume.empathic_voice.types.posted_language_model import PostedLanguageModel
from hume.empathic_voice.types.posted_user_defined_tool_spec import (
    PostedUserDefinedToolSpec,
)
from hume.empathic_voice.types.posted_voice import PostedVoice
from hume.empathic_voice.types.return_config import ReturnConfig
from hume.empathic_voice.types.return_user_defined_tool import ReturnUserDefinedTool
from hume.empathic_voice.types.session_settings import SessionSettings
from utilities.eval_data import EvalData

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


@pytest.mark.asyncio
@pytest.mark.voice
@pytest.mark.service
class TestServiceHumeVoiceClientChat:
    async def test_chat(
        self,
        eval_data: EvalData,
        hume_client: HumeClient,
        tmp_path_factory: pytest.TempPathFactory,
    ) -> None:
        data_url = eval_data["know-any-good-jokes"]
        data_filepath = tmp_path_factory.mktemp("data-dir") / "sample.wav"
        urlretrieve(data_url, data_filepath)

        async with hume_client.empathic_voice.chat.connect(
            options=AsyncChatConnectOptions(
                client_secret=os.getenv("HUME_CLIENT_SECRET")
            )
        ) as socket:
            await socket.send_session_settings(
                SessionSettings(
                    audio=AudioConfiguration(
                        encoding="linear16", sample_rate=16_000, channels=1
                    )
                )
            )

            await socket.send_file(data_filepath)
            messages = []
            async for message_str in socket:
                logger.info("Received message on socket")
                message = json.loads(message_str)

                assert (
                    "type" in message
                ), f"Expected message to have a 'type' field: {message}"

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

    def clean_up(
        self, hume_client: HumeClient, config: ReturnConfig, tool: ReturnUserDefinedTool
    ) -> None:
        hume_client.empathic_voice.configs.delete_config(config.id) # type: ignore
        hume_client.empathic_voice.tools.delete_tool(tool.id)
