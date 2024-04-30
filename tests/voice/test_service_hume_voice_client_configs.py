import logging
from typing import Optional
from uuid import uuid4

import pytest

from hume import HumeVoiceClient, VoiceConfig
from hume.error.hume_client_exception import HumeClientException

logger = logging.getLogger(__name__)


@pytest.fixture(name="voice_client", scope="module")
def voice_client_fixture(hume_api_key: str) -> HumeVoiceClient:
    return HumeVoiceClient(hume_api_key)


@pytest.mark.voice
@pytest.mark.service
class TestServiceHumeVoiceClientConfigs:
    UUID_REGEX = r"[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}"

    def test_config_operations(self, voice_client: HumeVoiceClient) -> None:
        # NOTE: This UUID can be removed when the API supports duplicate config names after deletion.
        name_uuid = str(uuid4())
        name = f"bogus-config-{name_uuid}"
        prompt = "you are a voice bot!"
        description = "this is just a bogus config."
        new_config = voice_client.create_config(name=name, prompt=prompt, description=description)
        self.check_config_fields(new_config, name, prompt, description)

        fetched_config = voice_client.get_config(new_config.id)
        self.check_config_fields(fetched_config, name, prompt, description)

        listed_configs = list(voice_client.iter_configs())
        n_configs = len(listed_configs)
        assert n_configs >= 1

        voice_client.delete_config(new_config.id)

        listed_configs = list(voice_client.iter_configs())
        assert len(listed_configs) == n_configs - 1

        match = f"Config not found with ID: {self.UUID_REGEX}"
        with pytest.raises(HumeClientException, match=match):
            voice_client.get_config(new_config.id)

    def check_config_fields(self, config: VoiceConfig, name: str, prompt: str, description: Optional[str]) -> None:
        assert config.name == name
        assert config.prompt == prompt
        assert config.description == description
