import json
import re
from pathlib import Path

import pytest

from hume import BatchJobResult, BatchJobStatus, HumeClientException


@pytest.fixture(scope="function")
def completed_result() -> BatchJobResult:
    response_filepath = Path(__file__).parent / "data" / "result-response-completed.json"
    with response_filepath.open() as f:
        response = json.load(f)
        return BatchJobResult.from_response(response)


@pytest.fixture(scope="function")
def queued_result() -> BatchJobResult:
    response_filepath = Path(__file__).parent / "data" / "result-response-queued.json"
    with response_filepath.open() as f:
        response = json.load(f)
        return BatchJobResult.from_response(response)


@pytest.fixture(scope="function")
def failed_result() -> BatchJobResult:
    response_filepath = Path(__file__).parent / "data" / "result-response-failed.json"
    with response_filepath.open() as f:
        response = json.load(f)
        return BatchJobResult.from_response(response)


@pytest.mark.batch
class TestBatchJobResult:

    def test_queued_status(self, queued_result: BatchJobResult):
        assert queued_result.status == BatchJobStatus.QUEUED

    def test_queued_download_fail(self, queued_result: BatchJobResult):

        message = "Could not download job artifacts. No artifacts found on job result."
        with pytest.raises(HumeClientException, match=re.escape(message)):
            queued_result.download_artifacts("fake-path")

        message = "Could not download job errors. No errors found on job result."
        with pytest.raises(HumeClientException, match=re.escape(message)):
            queued_result.download_errors("fake-path")

        message = "Could not download job predictions. No predictions found on job result."
        with pytest.raises(HumeClientException, match=re.escape(message)):
            queued_result.download_predictions("fake-path")

    def test_completed(self, completed_result: BatchJobResult):
        assert completed_result.status == BatchJobStatus.COMPLETED
        assert completed_result.predictions_url is not None
        assert completed_result.errors_url is not None
        assert completed_result.artifacts_url is not None

    def test_failed_message(self, failed_result: BatchJobResult):
        assert failed_result.status == BatchJobStatus.FAILED
        assert failed_result.get_error_message() == "user 'abcde' has exceeded their usage limit"

    def test_job_time_completed(self, completed_result: BatchJobResult):
        assert completed_result.get_run_time() == 3
        assert completed_result.get_start_time().strftime('%Y-%m-%d %H:%M:%S') == '2022-08-15 20:20:10'
        assert completed_result.get_end_time().strftime('%Y-%m-%d %H:%M:%S') == '2022-08-15 20:20:13'

    def test_job_time_failed(self, failed_result: BatchJobResult):
        assert failed_result.get_run_time() == 2
        assert failed_result.get_start_time().strftime('%Y-%m-%d %H:%M:%S') == '2022-09-21 19:56:39'
        assert failed_result.get_end_time().strftime('%Y-%m-%d %H:%M:%S') == '2022-09-21 19:56:41'

    def test_job_time_queued(self, queued_result: BatchJobResult):
        assert queued_result.get_run_time() is None
        assert queued_result.get_start_time().strftime('%Y-%m-%d %H:%M:%S') == '2022-08-15 20:20:10'
        assert queued_result.get_end_time() is None
