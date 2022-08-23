from unittest.mock import MagicMock

import pytest
from pytest import MonkeyPatch

from hume import BatchJob, HumeBatchClient


@pytest.fixture(scope="function")
def batch_client(monkeypatch: MonkeyPatch) -> HumeBatchClient:
    mock_start_job = MagicMock(return_value="temp-job-value")
    monkeypatch.setattr(HumeBatchClient, "_start_job", mock_start_job)
    client = HumeBatchClient("0000-0000-0000-0000")
    mock_start_job.return_value = BatchJob(client, "mock_job_id")
    return client


class TestHumeBatchClient:

    def test_face(self, batch_client: HumeBatchClient):
        mock_url = "mock-url"
        job = batch_client.submit_face(
            [mock_url],
            fps_pred=5,
            prob_threshold=0.24,
            identify_faces=True,
            min_face_size=78,
        )
        assert isinstance(job, BatchJob)
        assert job.id == "mock_job_id"
        batch_client._start_job.assert_called_once_with({
            "models": {
                "face": {
                    "fps_pred": 5,
                    "prob_threshold": 0.24,
                    "identify_faces": True,
                    "min_face_size": 78,
                },
            },
            "urls": [mock_url],
        })

    def test_burst(self, batch_client: HumeBatchClient):
        mock_url = "mock-url"
        job = batch_client.submit_burst([mock_url])
        assert isinstance(job, BatchJob)
        assert job.id == "mock_job_id"
        batch_client._start_job.assert_called_once_with({
            "models": {
                "burst": {},
            },
            "urls": [mock_url],
        })

    def test_prosody(self, batch_client: HumeBatchClient):
        mock_url = "mock-url"
        job = batch_client.submit_prosody(
            [mock_url],
            identify_speakers=True,
        )
        assert isinstance(job, BatchJob)
        assert job.id == "mock_job_id"
        batch_client._start_job.assert_called_once_with({
            "models": {
                "prosody": {
                    "identify_speakers": True,
                },
            },
            "urls": [mock_url],
        })

    def test_language(self, batch_client: HumeBatchClient):
        mock_url = "mock-url"
        job = batch_client.submit_language(
            [mock_url],
            sliding_window=False,
            identify_speakers=True,
        )
        assert isinstance(job, BatchJob)
        assert job.id == "mock_job_id"
        batch_client._start_job.assert_called_once_with({
            "models": {
                "language": {
                    "sliding_window": False,
                    "identify_speakers": True,
                },
            },
            "urls": [mock_url],
        })
