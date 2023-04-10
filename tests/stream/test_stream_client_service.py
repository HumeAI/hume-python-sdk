import logging
import re
from typing import Dict
from urllib.request import urlretrieve

import pytest
from pytest import TempPathFactory

from hume import HumeStreamClient, HumeClientException
from hume.models.config import FaceConfig, FacemeshConfig, LanguageConfig, ProsodyConfig

EvalData = Dict[str, str]

logger = logging.getLogger(__name__)


@pytest.fixture(scope="module")
def stream_client(hume_api_key: str) -> HumeStreamClient:
    return HumeStreamClient(hume_api_key)


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
        configs = [FaceConfig(identify_faces=True)]
        message = "HumeStreamClient initialized with invalid API key"
        with pytest.raises(HumeClientException, match=re.escape(message)):
            async with invalid_client.connect(configs):
                pass

    async def test_error_code_exception(
        self,
        eval_data: EvalData,
        stream_client: HumeStreamClient,
        tmp_path_factory: TempPathFactory,
    ):
        data_url = eval_data["image-obama-face"]
        data_filepath = tmp_path_factory.mktemp("data-dir") / "data-file"
        urlretrieve(data_url, data_filepath)

        configs = [ProsodyConfig()]
        async with stream_client.connect(configs) as websocket:
            message = ("hume(E0102): Streaming payload configured with model type 'prosody', "
                       "which is not supported for the detected file type 'image'.")
            with pytest.raises(HumeClientException, match=re.escape(message)):
                await websocket.send_file(data_filepath)
