import re
from unittest.mock import Mock

import pytest

from hume import BatchJob, BatchJobInfo, BatchJobState, BatchJobStatus
from hume.models import ModelType
from hume.models.config import FaceConfig


@pytest.fixture(scope="function")
def batch_client() -> Mock:
    mock_client = Mock()
    job_info = BatchJobInfo(
        configs={
            ModelType.FACE: FaceConfig(),
        },
        urls=["mock-url"],
        files=["mock-file"],
        state=BatchJobState(
            BatchJobStatus.FAILED,
            created_timestamp_ms=0,
            started_timestamp_ms=1,
            ended_timestamp_ms=2,
        ),
    )
    mock_client.get_job_info = Mock(return_value=job_info)
    return mock_client


@pytest.mark.batch
class TestBatchJob:

    def test_job_id(self, batch_client: Mock):
        mock_job_id = "mock-job-id"
        job = BatchJob(batch_client, mock_job_id)
        assert job.id == mock_job_id

    def test_invalid_await_timeout(self, batch_client: Mock):
        job = BatchJob(batch_client, "mock-job-id")

        message = "timeout must be at least 1 second"
        with pytest.raises(ValueError, match=re.escape(message)):
            job.await_complete(timeout=0)

    def test_get_info(self, batch_client: Mock):
        job = BatchJob(batch_client, "mock-job-id")
        info = job.get_info()
        assert info.state.status == BatchJobStatus.FAILED

    def test_get_status(self, batch_client: Mock):
        job = BatchJob(batch_client, "mock-job-id")
        status = job.get_status()
        assert status == BatchJobStatus.FAILED

    def test_await_complete(self, batch_client: Mock):
        job = BatchJob(batch_client, "mock-job-id")
        info = job.await_complete()
        assert info.state.status == BatchJobStatus.FAILED
