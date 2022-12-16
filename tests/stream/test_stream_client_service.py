import logging
import os
from typing import Dict
from urllib.request import urlretrieve

import pytest
from pytest import TempPathFactory

from hume import HumeStreamClient, HumeClientError
from hume.config import FaceConfig, FacemeshConfig, LanguageConfig

EvalData = Dict[str, str]

logger = logging.getLogger(__name__)


@pytest.fixture(scope="module")
def stream_client() -> HumeStreamClient:
    api_key = os.getenv("HUME_DEV_API_KEY")
    if api_key is None:
        raise ValueError("Cannot construct HumeStreamClient, HUME_DEV_API_KEY variable not set.")

    return HumeStreamClient(api_key)


@pytest.mark.asyncio
@pytest.mark.stream
@pytest.mark.service
class TestHumeStreamClientService:

    async def test_send_file(
        self,
        eval_data: EvalData,
        stream_client: HumeStreamClient,
        tmp_path_factory: TempPathFactory,
    ):
        data_url = eval_data["image-obama-face"]
        data_filepath = tmp_path_factory.mktemp("data-dir") / "data-file"
        urlretrieve(data_url, data_filepath)

        configs = [FaceConfig(identify_faces=True)]
        async with stream_client.connect(configs) as websocket:
            predictions = await websocket.send_file(data_filepath)
            assert predictions is not None

    async def test_send_text(self, stream_client: HumeStreamClient):
        sample_text = "Hello! I hope this test works!"
        configs = [LanguageConfig()]
        async with stream_client.connect(configs) as websocket:
            predictions = await websocket.send_text(sample_text)
            assert predictions is not None

    async def test_send_facemesh(self, stream_client: HumeStreamClient):
        meshes = [[[0, 0, 0]] * 478]
        configs = [FacemeshConfig()]
        async with stream_client.connect(configs) as websocket:
            predictions = await websocket.send_facemesh(meshes)
            assert predictions is not None

    async def test_invalid_api_key(self):
        invalid_client = HumeStreamClient("invalid-api-key")
        message = "Client initialized with invalid API key"
        configs = [FaceConfig(identify_faces=True)]
        with pytest.raises(HumeClientError, match=message):
            async with invalid_client.connect(configs):
                pass
