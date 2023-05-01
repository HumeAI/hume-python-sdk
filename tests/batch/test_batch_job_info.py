import json
from pathlib import Path

import pytest

from hume import BatchJobInfo, BatchJobStatus


@pytest.fixture(scope="function")
def completed_info() -> BatchJobInfo:
    response_filepath = Path(__file__).parent / "data" / "info-response-completed.json"
    with response_filepath.open() as f:
        response = json.load(f)
        return BatchJobInfo.from_response(response)


@pytest.fixture(scope="function")
def queued_info() -> BatchJobInfo:
    response_filepath = Path(__file__).parent / "data" / "info-response-queued.json"
    with response_filepath.open() as f:
        response = json.load(f)
        return BatchJobInfo.from_response(response)


@pytest.fixture(scope="function")
def failed_info() -> BatchJobInfo:
    response_filepath = Path(__file__).parent / "data" / "info-response-failed.json"
    with response_filepath.open() as f:
        response = json.load(f)
        return BatchJobInfo.from_response(response)


@pytest.mark.batch
class TestBatchJobInfo:

    def test_queued_status(self, queued_info: BatchJobInfo):
        assert queued_info.state.status == BatchJobStatus.QUEUED

    def test_completed(self, completed_info: BatchJobInfo):
        assert completed_info.state.status == BatchJobStatus.COMPLETED
        assert completed_info.configs is not None
        assert completed_info.urls is not None
        assert completed_info.files is not None
        assert completed_info.callback_url is not None
        assert completed_info.notify is not None

    def test_job_time_completed(self, completed_info: BatchJobInfo):
        assert completed_info.state.get_created_time().strftime('%Y-%m-%d %H:%M:%S') == '2022-08-15 20:20:10'
        assert completed_info.state.get_started_time().strftime('%Y-%m-%d %H:%M:%S') == '2022-08-15 20:20:12'
        assert completed_info.state.get_ended_time().strftime('%Y-%m-%d %H:%M:%S') == '2022-08-15 20:20:15'
        assert completed_info.state.get_run_time_ms() == 3000

    def test_job_time_failed(self, failed_info: BatchJobInfo):
        assert failed_info.state.get_created_time().strftime('%Y-%m-%d %H:%M:%S') == '2022-08-15 20:20:11'
        assert failed_info.state.get_started_time().strftime('%Y-%m-%d %H:%M:%S') == '2022-08-15 20:20:14'
        assert failed_info.state.get_ended_time().strftime('%Y-%m-%d %H:%M:%S') == '2022-08-15 20:20:16'
        assert failed_info.state.get_run_time_ms() == 2000

    def test_job_time_queued(self, queued_info: BatchJobInfo):
        assert queued_info.state.get_created_time().strftime('%Y-%m-%d %H:%M:%S') == '2022-08-15 20:20:15'
        assert queued_info.state.get_started_time() is None
        assert queued_info.state.get_ended_time() is None
        assert queued_info.state.get_run_time_ms() is None
