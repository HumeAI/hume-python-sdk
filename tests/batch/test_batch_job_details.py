import json
from pathlib import Path

import pytest

from hume import BatchJobDetails, BatchJobStatus


@pytest.fixture(scope="function")
def completed_details() -> BatchJobDetails:
    response_filepath = Path(__file__).parent / "data" / "details-response-completed.json"
    with response_filepath.open() as f:
        response = json.load(f)
        return BatchJobDetails.from_response(response)


@pytest.fixture(scope="function")
def queued_details() -> BatchJobDetails:
    response_filepath = Path(__file__).parent / "data" / "details-response-queued.json"
    with response_filepath.open() as f:
        response = json.load(f)
        return BatchJobDetails.from_response(response)


@pytest.fixture(scope="function")
def failed_details() -> BatchJobDetails:
    response_filepath = Path(__file__).parent / "data" / "details-response-failed.json"
    with response_filepath.open() as f:
        response = json.load(f)
        return BatchJobDetails.from_response(response)


@pytest.mark.batch
class TestBatchJobDetails:

    def test_queued_status(self, queued_details: BatchJobDetails):
        assert queued_details.get_status() == BatchJobStatus.QUEUED

    def test_completed(self, completed_details: BatchJobDetails):
        assert completed_details.get_status() == BatchJobStatus.COMPLETED
        assert completed_details.configs is not None
        assert completed_details.urls is not None
        assert completed_details.files is not None
        assert completed_details.callback_url is not None
        assert completed_details.notify is not None

    def test_job_time_completed(self, completed_details: BatchJobDetails):
        assert completed_details.get_created_time().strftime('%Y-%m-%d %H:%M:%S') == '2022-08-15 20:20:10'
        assert completed_details.get_started_time().strftime('%Y-%m-%d %H:%M:%S') == '2022-08-15 20:20:12'
        assert completed_details.get_ended_time().strftime('%Y-%m-%d %H:%M:%S') == '2022-08-15 20:20:15'
        assert completed_details.get_run_time_ms() == 3000

    def test_job_time_failed(self, failed_details: BatchJobDetails):
        assert failed_details.get_created_time().strftime('%Y-%m-%d %H:%M:%S') == '2022-08-15 20:20:11'
        assert failed_details.get_started_time().strftime('%Y-%m-%d %H:%M:%S') == '2022-08-15 20:20:14'
        assert failed_details.get_ended_time().strftime('%Y-%m-%d %H:%M:%S') == '2022-08-15 20:20:16'
        assert failed_details.get_run_time_ms() == 2000

    def test_job_time_queued(self, queued_details: BatchJobDetails):
        assert queued_details.get_created_time().strftime('%Y-%m-%d %H:%M:%S') == '2022-08-15 20:20:15'
        assert queued_details.get_started_time() is None
        assert queued_details.get_ended_time() is None
        assert queued_details.get_run_time_ms() is None
