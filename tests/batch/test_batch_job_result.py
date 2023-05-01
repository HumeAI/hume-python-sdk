import json
import re
from pathlib import Path

import pytest

from hume import BatchJobInfo, BatchJobStatus, HumeClientException


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
        assert queued_info.status == BatchJobStatus.QUEUED

    def test_queued_download_fail(self, queued_info: BatchJobInfo):

        message = "Could not download job artifacts. No artifacts found for job."
        with pytest.raises(HumeClientException, match=re.escape(message)):
            queued_info.download_artifacts("fake-path")

        message = "Could not download job errors. No errors found for job."
        with pytest.raises(HumeClientException, match=re.escape(message)):
            queued_info.download_errors("fake-path")

        message = "Could not download job predictions. No predictions found for job."
        with pytest.raises(HumeClientException, match=re.escape(message)):
            queued_info.download_predictions("fake-path")

    def test_completed(self, completed_info: BatchJobInfo):
        assert completed_info.state.status == BatchJobStatus.COMPLETED
        assert completed_info.configs is not None
        assert completed_info.urls is not None
        assert completed_info.files is not None
        assert completed_info.callback_url is not None
        assert completed_info.notify is not None

    def test_failed_message(self, failed_info: BatchJobInfo):
        assert failed_info.state.status == BatchJobStatus.FAILED
        assert failed_info.get_error_message() == "user 'abcde' has exceeded their usage limit"

    def test_job_time_completed(self, completed_info: BatchJobInfo):
        assert completed_info.state.get_run_time() == 3
        assert completed_info.state.get_created_time().strftime('%Y-%m-%d %H:%M:%S') == '2022-08-15 20:20:10'
        assert completed_info.state.get_started_time().strftime('%Y-%m-%d %H:%M:%S') == '2022-08-15 20:20:10'
        assert completed_info.state.get_ended_time().strftime('%Y-%m-%d %H:%M:%S') == '2022-08-15 20:20:13'

    def test_job_time_failed(self, failed_info: BatchJobInfo):
        assert failed_info.state.get_run_time() == 2
        assert failed_info.state.get_created_time().strftime('%Y-%m-%d %H:%M:%S') == '2022-08-15 20:20:10'
        assert failed_info.state.get_started_time().strftime('%Y-%m-%d %H:%M:%S') == '2022-09-21 19:56:39'
        assert failed_info.state.get_ended_time().strftime('%Y-%m-%d %H:%M:%S') == '2022-09-21 19:56:41'

    def test_job_time_queued(self, queued_info: BatchJobInfo):
        assert queued_info.state.get_run_time() is None
        assert queued_info.state.get_created_time().strftime('%Y-%m-%d %H:%M:%S') == '2022-08-15 20:20:10'
        assert queued_info.state.get_started_time().strftime('%Y-%m-%d %H:%M:%S') == '2022-08-15 20:20:10'
        assert queued_info.state.get_ended_time() is None
