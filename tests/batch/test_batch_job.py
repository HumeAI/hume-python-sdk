from unittest.mock import Mock

import pytest

from hume import BatchJob, BatchJobResult, BatchJobStatus, ModelType
from hume._common.config import FaceConfig


@pytest.fixture(scope="function")
def batch_client() -> Mock:
    mock_client = Mock()
    job_result = BatchJobResult(
        configs={
            ModelType.FACE: FaceConfig(),
        },
        urls="mock-url",
        status=BatchJobStatus.FAILED,
    )
    mock_client.get_job_result = Mock(return_value=job_result)
    return mock_client


@pytest.mark.batch
class TestBatchJob:

    def test_job_id(self, batch_client: Mock):
        mock_job_id = "mock-job-id"
        job = BatchJob(batch_client, mock_job_id)
        assert job.id == mock_job_id

    def test_invalid_await_timeout(self, batch_client: Mock):
        job = BatchJob(batch_client, "mock-job-id")
        with pytest.raises(ValueError, match="timeout must be at least 1 second"):
            job.await_complete(timeout=0)

    def test_get_result(self, batch_client: Mock):
        job = BatchJob(batch_client, "mock-job-id")
        result = job.get_result()
        assert result.status == BatchJobStatus.FAILED

    def test_get_status(self, batch_client: Mock):
        job = BatchJob(batch_client, "mock-job-id")
        status = job.get_status()
        assert status == BatchJobStatus.FAILED

    def test_await_complete(self, batch_client: Mock):
        job = BatchJob(batch_client, "mock-job-id")
        result = job.await_complete()
        assert result.status == BatchJobStatus.FAILED
