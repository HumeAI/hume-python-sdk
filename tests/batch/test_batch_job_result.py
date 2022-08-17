import json
from pathlib import Path

import pytest

from hume import BatchJobResult, BatchJobStatus, HumeClientError


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


class TestBatchJobResult:

    def test_queued_status(self, queued_result: BatchJobResult):
        assert queued_result.status == BatchJobStatus.QUEUED

    def test_queued_download_fail(self, queued_result: BatchJobResult):

        message = "Could not download job artifacts. No artifacts found on job result"
        with pytest.raises(HumeClientError, match=message):
            queued_result.download_artifacts("fake-path")

        message = "Could not download job errors. No errors found on job result."
        with pytest.raises(HumeClientError, match=message):
            queued_result.download_errors("fake-path")

        message = "Could not download job predictions. No predictions found on job result."
        with pytest.raises(HumeClientError, match=message):
            queued_result.download_predictions("fake-path")

    def test_completed(self, completed_result: BatchJobResult):
        assert completed_result.status == BatchJobStatus.COMPLETED
        assert completed_result.predictions_url is not None
        assert completed_result.errors_url is not None
        assert completed_result.artifacts_url is not None
