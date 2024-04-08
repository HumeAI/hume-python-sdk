from urllib.request import urlretrieve

import pytest
from pytest import TempPathFactory

from hume import HumeStreamClient
from hume.models.config import FaceConfig, LanguageConfig
from utilities.eval_data import EvalData


@pytest.fixture(name="stream_client", scope="module")
def stream_client_fixture(hume_api_key: str) -> HumeStreamClient:
    return HumeStreamClient(hume_api_key)


@pytest.mark.asyncio
@pytest.mark.stream
@pytest.mark.service
class TestServiceStreamScenarios:

    async def test_facs_and_descriptions(
        self,
        eval_data: EvalData,
        stream_client: HumeStreamClient,
        tmp_path_factory: TempPathFactory,
    ) -> None:
        data_url = eval_data["image-obama-face"]
        data_filepath = tmp_path_factory.mktemp("data-dir") / "data-file"
        urlretrieve(data_url, data_filepath)

        configs = [FaceConfig(facs={}, descriptions={})]
        async with stream_client.connect(configs) as websocket:
            result = await websocket.send_file(data_filepath)
            predictions = result["face"]["predictions"]
            assert "facs" in predictions[0]
            assert "descriptions" in predictions[0]

    async def test_sentiment_and_toxicity(self, stream_client: HumeStreamClient) -> None:
        sample_text = "Hello! I hope this test works!"
        configs = [LanguageConfig(sentiment={}, toxicity={})]
        async with stream_client.connect(configs) as websocket:
            result = await websocket.send_text(sample_text)
            predictions = result["language"]["predictions"]
            assert "sentiment" in predictions[0]
            assert "toxicity" in predictions[0]
