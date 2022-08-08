import json
import logging
import os
from typing import Dict

import pytest
from pytest import TempPathFactory

from hume import HumeBatchClient, BatchJob

EvalData = Dict[str, str]

logger = logging.getLogger(__name__)


@pytest.fixture(scope="module")
def batch_client() -> HumeBatchClient:
    api_key = os.getenv("HUME_PLATFORM_API_KEY")
    if api_key is None:
        raise ValueError("Cannot construct HumeBatchClient, HUME_PLATFORM_API_KEY variable not set.")

    return HumeBatchClient(api_key)


@pytest.fixture(scope="module")
def eval_data() -> EvalData:
    base_url = "https://storage.googleapis.com/hume-test-data"
    return {
        "image-obama-face": f"{base_url}/image/obama.png",
        "burst-amusement-009": f"{base_url}/audio/burst-amusement-009.mp3",
        "prosody-horror-1051": f"{base_url}/audio/prosody-horror-1051.mp3",
        "text-happy-place": f"{base_url}/text/happy.txt",
    }


@pytest.mark.service
class TestHumeBatchClientService:

    def test_face(self, eval_data: EvalData, batch_client: HumeBatchClient, tmp_path_factory: TempPathFactory):
        data_url = eval_data["image-obama-face"]
        download_filepath = tmp_path_factory.mktemp("results") / "results.json"
        job = batch_client.submit_face([data_url])
        assert isinstance(job, BatchJob)
        assert len(job.id) == 32
        logger.info(f"Running test job {job.id}")
        result = job.await_complete()
        result.download_predictions(download_filepath)
        with download_filepath.open() as f:
            json.load(f)

    def test_burst(self, eval_data: EvalData, batch_client: HumeBatchClient, tmp_path_factory: TempPathFactory):
        data_url = eval_data["burst-amusement-009"]
        download_filepath = tmp_path_factory.mktemp("results") / "results.json"
        job = batch_client.submit_burst([data_url])
        assert isinstance(job, BatchJob)
        assert len(job.id) == 32
        logger.info(f"Running test job {job.id}")
        result = job.await_complete()
        result.download_predictions(download_filepath)
        with download_filepath.open() as f:
            json.load(f)

    def test_prosody(self, eval_data: EvalData, batch_client: HumeBatchClient, tmp_path_factory: TempPathFactory):
        data_url = eval_data["prosody-horror-1051"]
        download_filepath = tmp_path_factory.mktemp("results") / "results.json"
        job = batch_client.submit_prosody([data_url])
        assert isinstance(job, BatchJob)
        assert len(job.id) == 32
        logger.info(f"Running test job {job.id}")
        result = job.await_complete()
        result.download_predictions(download_filepath)
        with download_filepath.open() as f:
            json.load(f)

    def test_language(self, eval_data: EvalData, batch_client: HumeBatchClient, tmp_path_factory: TempPathFactory):
        data_url = eval_data["text-happy-place"]
        download_filepath = tmp_path_factory.mktemp("results") / "results.json"
        job = batch_client.submit_language([data_url])
        assert isinstance(job, BatchJob)
        assert len(job.id) == 32
        logger.info(f"Running test job {job.id}")
        result = job.await_complete()
        result.download_predictions(download_filepath)
        with download_filepath.open() as f:
            json.load(f)
