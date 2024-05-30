from urllib.request import urlretrieve

import pytest
from pytest import TempPathFactory

from hume.client import HumeClient
from hume.expression_measurement.stream.socket_client import AsyncStreamConnectOptions
from hume.expression_measurement.stream.types import StreamDataModels, StreamDataModelsLanguage, StreamDataModelsFace
from utilities.eval_data import EvalData


@pytest.mark.asyncio
@pytest.mark.stream
@pytest.mark.service
class TestServiceStreamScenarios:
    async def test_facs_and_descriptions(
        self,
        eval_data: EvalData,
        hume_client: HumeClient,
        tmp_path_factory: TempPathFactory,
    ) -> None:
        data_url = eval_data["image-obama-face"]
        data_filepath = tmp_path_factory.mktemp("data-dir") / "data-file"
        urlretrieve(data_url, data_filepath)

        async with hume_client.expression_measurement.stream.connect(
            options=AsyncStreamConnectOptions(
                config=StreamDataModels(face=StreamDataModelsFace(facs={}, descriptions={}))
            )
        ) as websocket:
            result = await websocket.send_file(data_filepath)
            predictions = result.face.predictions
            assert predictions[0].facs is not None
            assert predictions[0].descriptions is not None

    async def test_sentiment_and_toxicity(self, hume_client: HumeClient) -> None:
        sample_text = "Hello! I hope this test works!"
        async with hume_client.expression_measurement.stream.connect(
            options=AsyncStreamConnectOptions(
                config=StreamDataModels(language=StreamDataModelsLanguage(sentiment={}, toxicity={}))
            )
        ) as websocket:
            result = await websocket.send_text(sample_text)
            predictions = result.language.predictions
            assert predictions[0].sentiment is not None
            assert predictions[0].toxicity is not None
