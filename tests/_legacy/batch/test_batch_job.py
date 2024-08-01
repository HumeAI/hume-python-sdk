import re
from unittest.mock import Mock

import pytest

from hume.legacy import BatchJob, BatchJobDetails, BatchJobState, BatchJobStatus, HumeClientException
from hume.legacy.models import ModelType
from hume.legacy.models.config import FaceConfig


@pytest.fixture(name="batch_client", scope="function")
def batch_client_fixture() -> Mock:
    mock_client = Mock()
    job_details = BatchJobDetails(
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
    mock_client.get_job_details = Mock(return_value=job_details)
    return mock_client


@pytest.mark.batch
class TestBatchJob:

    def test_job_id(self, batch_client: Mock) -> None:
        mock_job_id = "mock-job-id"
        job = BatchJob(batch_client, mock_job_id)
        assert job.id == mock_job_id

    def test_invalid_await_timeout(self, batch_client: Mock) -> None:
        job = BatchJob(batch_client, "mock-job-id")

        message = "timeout must be at least 1 second"
        with pytest.raises(ValueError, match=re.escape(message)):
            job.await_complete(timeout=0)

    def test_get_details(self, batch_client: Mock) -> None:
        job = BatchJob(batch_client, "mock-job-id")
        details = job.get_details()
        assert details.state.status == BatchJobStatus.FAILED

    def test_get_status(self, batch_client: Mock) -> None:
        job = BatchJob(batch_client, "mock-job-id")
        status = job.get_status()
        assert status == BatchJobStatus.FAILED

    def test_await_complete(self, batch_client: Mock) -> None:
        job = BatchJob(batch_client, "mock-job-id")
        details = job.await_complete()
        assert details.state.status == BatchJobStatus.FAILED

    def test_raise_on_failed(self, batch_client: Mock) -> None:
        job = BatchJob(batch_client, "mock-job-id")
        message = "BatchJob mock-job-id failed."
        with pytest.raises(HumeClientException, match=re.escape(message)):
            job.await_complete(raise_on_failed=True)
