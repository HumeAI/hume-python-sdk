import json
from datetime import datetime
from pathlib import Path
from typing import Optional

import pytest

from hume import BatchJobDetails, BatchJobStatus


@pytest.fixture(name="completed_details", scope="function")
def completed_details_fixture() -> BatchJobDetails:
    response_filepath = Path(__file__).parent / "data" / "details-response-completed.json"
    with response_filepath.open() as f:
        response = json.load(f)
        return BatchJobDetails.from_response(response)


@pytest.fixture(name="queued_details", scope="function")
def queued_details_fixture() -> BatchJobDetails:
    response_filepath = Path(__file__).parent / "data" / "details-response-queued.json"
    with response_filepath.open() as f:
        response = json.load(f)
        return BatchJobDetails.from_response(response)


@pytest.fixture(name="failed_details", scope="function")
def failed_details_fixture() -> BatchJobDetails:
    response_filepath = Path(__file__).parent / "data" / "details-response-failed.json"
    with response_filepath.open() as f:
        response = json.load(f)
        return BatchJobDetails.from_response(response)


@pytest.mark.batch
class TestBatchJobDetails:

    def test_queued_status(self, queued_details: BatchJobDetails) -> None:
        assert queued_details.get_status() == BatchJobStatus.QUEUED

    def test_completed(self, completed_details: BatchJobDetails) -> None:
        assert completed_details.get_status() == BatchJobStatus.COMPLETED
        assert completed_details.configs is not None
        assert completed_details.urls is not None
        assert completed_details.files is not None
        assert completed_details.callback_url is not None
        assert completed_details.notify is not None

    def test_job_time_completed(self, completed_details: BatchJobDetails) -> None:
        self.check_time(completed_details.get_created_time(), "2022-08-15 20:20:10")
        self.check_time(completed_details.get_started_time(), "2022-08-15 20:20:12")
        self.check_time(completed_details.get_ended_time(), "2022-08-15 20:20:15")
        assert completed_details.get_run_time_ms() == 3000

    def test_job_time_failed(self, failed_details: BatchJobDetails) -> None:
        self.check_time(failed_details.get_created_time(), "2022-08-15 20:20:11")
        self.check_time(failed_details.get_started_time(), "2022-08-15 20:20:14")
        self.check_time(failed_details.get_ended_time(), "2022-08-15 20:20:16")
        assert failed_details.get_run_time_ms() == 2000

    def test_job_time_queued(self, queued_details: BatchJobDetails) -> None:
        self.check_time(queued_details.get_created_time(), "2022-08-15 20:20:15")
        assert queued_details.get_started_time() is None
        assert queued_details.get_ended_time() is None
        assert queued_details.get_run_time_ms() is None

    def check_time(self, date: Optional[datetime], formatted_date: str) -> None:
        assert date is not None
        assert date.strftime("%Y-%m-%d %H:%M:%S") == formatted_date
