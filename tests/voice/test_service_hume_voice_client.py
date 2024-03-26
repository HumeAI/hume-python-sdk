import logging
from typing import Optional
from urllib.request import urlretrieve
from uuid import uuid4

import pytest
from pydub import AudioSegment

from hume import HumeVoiceClient, VoiceConfig
from hume.error.hume_client_exception import HumeClientException
from utilities.eval_data import EvalData

logger = logging.getLogger(__name__)


@pytest.fixture(name="voice_client", scope="module")
def voice_client_fixture(hume_api_key: str) -> HumeVoiceClient:
    return HumeVoiceClient(hume_api_key)


@pytest.mark.asyncio
@pytest.mark.voice
@pytest.mark.service
class TestServiceHumeVoiceClient:
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

    @pytest.mark.skip("TODO: Implement")
    async def test_chat(
        self,
        eval_data: EvalData,
        voice_client: HumeVoiceClient,
        tmp_path_factory: pytest.TempPathFactory,
    ) -> None:
        data_url = eval_data["tell-me-a-joke"]
        data_filepath = tmp_path_factory.mktemp("data-dir") / "sample.wav"
        urlretrieve(data_url, data_filepath)
        silence_filepath = tmp_path_factory.mktemp("data-dir") / "silence.wav"
        AudioSegment.silent(duration=2000).export(silence_filepath, format="wav")

        async with voice_client.connect() as socket:
            await socket.send_file(data_filepath)
            await socket.send_file(silence_filepath)
            async for message in socket:
                if not isinstance(message, bytes):
                    print(message)
            await socket.send_file(silence_filepath)
