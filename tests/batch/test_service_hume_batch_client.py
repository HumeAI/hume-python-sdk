import json
import logging
import re
from datetime import datetime
from pathlib import Path
from typing import Dict

import pytest
from pytest import TempPathFactory

from hume import BatchJob, BatchJobResult, HumeBatchClient, HumeClientException
from hume.models.config import BurstConfig, FaceConfig, LanguageConfig, ProsodyConfig

EvalData = Dict[str, str]

logger = logging.getLogger(__name__)


@pytest.fixture(scope="module")
def batch_client(hume_api_key: str) -> HumeBatchClient:
    return HumeBatchClient(hume_api_key)


@pytest.mark.batch
@pytest.mark.service
class TestServiceHumeBatchClient:

    def test_face(self, eval_data: EvalData, batch_client: HumeBatchClient, tmp_path_factory: TempPathFactory):
        data_url = eval_data["image-obama-face"]
        config = FaceConfig(fps_pred=5, prob_threshold=0.24, identify_faces=True, min_face_size=78)
        job = batch_client.submit_job([data_url], [config])
        assert isinstance(job, BatchJob)
        assert len(job.id) == 32
        logger.info(f"Running test job {job.id}")
        result = job.await_complete()
        job_files_dir = tmp_path_factory.mktemp("job-files")
        self.check_result(result, job_files_dir)

    def test_burst(self, eval_data: EvalData, batch_client: HumeBatchClient, tmp_path_factory: TempPathFactory):
        data_url = eval_data["burst-amusement-009"]
        config = BurstConfig()
        job = batch_client.submit_job([data_url], [config])
        assert isinstance(job, BatchJob)
        assert len(job.id) == 32
        logger.info(f"Running test job {job.id}")
        result = job.await_complete()
        job_files_dir = tmp_path_factory.mktemp("job-files")
        self.check_result(result, job_files_dir)

    def test_prosody(self, eval_data: EvalData, batch_client: HumeBatchClient, tmp_path_factory: TempPathFactory):
        data_url = eval_data["prosody-horror-1051"]
        config = ProsodyConfig(identify_speakers=True)
        job = batch_client.submit_job([data_url], [config])
        assert isinstance(job, BatchJob)
        assert len(job.id) == 32
        logger.info(f"Running test job {job.id}")
        result = job.await_complete()
        job_files_dir = tmp_path_factory.mktemp("job-files")
        self.check_result(result, job_files_dir)

    def test_language(self, eval_data: EvalData, batch_client: HumeBatchClient, tmp_path_factory: TempPathFactory):
        data_url = eval_data["text-happy-place"]
        config = LanguageConfig(granularity="word", identify_speakers=True)
        job = batch_client.submit_job([data_url], [config])
        assert isinstance(job, BatchJob)
        assert len(job.id) == 32
        logger.info(f"Running test job {job.id}")
        result = job.await_complete()
        job_files_dir = tmp_path_factory.mktemp("job-files")
        self.check_result(result, job_files_dir)

    def test_client_invalid_api_key(self, eval_data: EvalData):
        invalid_client = HumeBatchClient("invalid-api-key")
        data_url = eval_data["image-obama-face"]
        message = "HumeBatchClient initialized with invalid API key."
        with pytest.raises(HumeClientException, match=re.escape(message)):
            invalid_client.submit_job([data_url], [FaceConfig()])

    def test_job_invalid_api_key(self, eval_data: EvalData, batch_client: HumeBatchClient):
        data_url = eval_data["image-obama-face"]
        job = batch_client.submit_job([data_url], [FaceConfig()])
        invalid_client = HumeBatchClient("invalid-api-key")
        message = "HumeBatchClient initialized with invalid API key."
        with pytest.raises(HumeClientException, match=re.escape(message)):
            rehydrated_job = BatchJob(invalid_client, job.id)
            rehydrated_job.await_complete(10)

    def check_result(self, result: BatchJobResult, job_files_dir: Path):
        predictions_filepath = job_files_dir / "results.json"
        result.download_predictions(predictions_filepath)
        with predictions_filepath.open() as f:
            json.load(f)

        artifacts_filepath = job_files_dir / "artifacts"
        result.download_artifacts(artifacts_filepath)

        error_filepath = job_files_dir / "errors.json"
        result.download_errors(error_filepath)

        error_message = result.get_error_message()
        assert error_message is None

        assert isinstance(result.get_run_time(), int)
        assert isinstance(result.get_start_time(), datetime)
        assert isinstance(result.get_end_time(), datetime)
