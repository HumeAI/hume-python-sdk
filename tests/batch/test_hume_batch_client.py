from unittest.mock import MagicMock

import pytest
from pytest import MonkeyPatch

from hume import BatchJob, HumeBatchClient
from hume.models.config import BurstConfig, FaceConfig, LanguageConfig, ProsodyConfig


@pytest.fixture(scope="function")
def batch_client(monkeypatch: MonkeyPatch) -> HumeBatchClient:
    mock_submit_request = MagicMock(return_value="temp-job-value")
    monkeypatch.setattr(HumeBatchClient, "_submit_job", mock_submit_request)
    client = HumeBatchClient("0000-0000-0000-0000", timeout=15)
    mock_submit_request.return_value = BatchJob(client, "mock-job-id")
    return client


@pytest.mark.batch
class TestHumeBatchClient:

    def test_face(self, batch_client: HumeBatchClient):
        mock_url = "mock-url"
        config = FaceConfig(fps_pred=5, prob_threshold=0.24, identify_faces=True, min_face_size=78)
        job = batch_client.submit_job([mock_url], [config])
        assert isinstance(job, BatchJob)
        assert job.id == "mock-job-id"
        batch_client._submit_job.assert_called_once_with(
            {
                "models": {
                    "face": {
                        "fps_pred": 5,
                        "prob_threshold": 0.24,
                        "identify_faces": True,
                        "min_face_size": 78,
                    },
                },
                "urls": [mock_url],
            },
            None,
        )

    def test_burst(self, batch_client: HumeBatchClient):
        mock_url = "mock-url"
        config = BurstConfig()
        job = batch_client.submit_job([mock_url], [config])
        assert isinstance(job, BatchJob)
        assert job.id == "mock-job-id"
        batch_client._submit_job.assert_called_once_with(
            {
                "models": {
                    "burst": {},
                },
                "urls": [mock_url],
            },
            None,
        )

    def test_prosody(self, batch_client: HumeBatchClient):
        mock_url = "mock-url"
        config = ProsodyConfig(identify_speakers=True)
        job = batch_client.submit_job([mock_url], [config])
        assert isinstance(job, BatchJob)
        assert job.id == "mock-job-id"
        batch_client._submit_job.assert_called_once_with(
            {
                "models": {
                    "prosody": {
                        "identify_speakers": True,
                    },
                },
                "urls": [mock_url],
            },
            None,
        )

    def test_language(self, batch_client: HumeBatchClient):
        mock_url = "mock-url"
        config = LanguageConfig(granularity="word", identify_speakers=True)
        job = batch_client.submit_job([mock_url], [config])
        assert isinstance(job, BatchJob)
        assert job.id == "mock-job-id"
        batch_client._submit_job.assert_called_once_with(
            {
                "models": {
                    "language": {
                        "granularity": "word",
                        "identify_speakers": True,
                    },
                },
                "urls": [mock_url],
            },
            None,
        )

    def test_get_job(self, batch_client: HumeBatchClient):
        job = batch_client.get_job("mock-job-id")
        assert job.id == "mock-job-id"
