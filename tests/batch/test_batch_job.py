from unittest.mock import MagicMock

import pytest
from pytest import MonkeyPatch

from hume import BatchJob, HumeBatchClient


@pytest.fixture(scope="function")
def batch_client(monkeypatch: MonkeyPatch) -> HumeBatchClient:
    mock_start_job = MagicMock(return_value="fake-job")
    monkeypatch.setattr(HumeBatchClient, "_start_job", mock_start_job)
    return HumeBatchClient("0000-0000-0000-0000")


class TestBatchJob:

    def test_job_id(self, batch_client: HumeBatchClient):
        mock_job_id = "mock-job-id"
        job = BatchJob(batch_client, mock_job_id)
        assert job.id == mock_job_id

    def test_invalid_await_timeout(self, batch_client: HumeBatchClient):
        job = BatchJob(batch_client, "mock_job_id")
        with pytest.raises(ValueError, match="timeout must be at least 1 second"):
            job.await_complete(timeout=0)
