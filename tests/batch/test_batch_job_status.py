import re

import pytest

from hume import BatchJobStatus


@pytest.mark.batch
class TestBatchJobStatus:

    def test_update(self) -> None:
        # Note: If another status is added to the enum make sure to update parametrized tests below:
        # - test_continuity
        # - test_is_terminal
        assert len(BatchJobStatus) == 4

    @pytest.mark.parametrize(
        "status_str",
        [
            "COMPLETED",
            "FAILED",
            "IN_PROGRESS",
            "QUEUED",
        ],
    )
    def test_continuity(self, status_str: str) -> None:
        assert BatchJobStatus[status_str].value == status_str

    def test_from_str(self) -> None:
        assert BatchJobStatus.from_str("COMPLETED") == BatchJobStatus.COMPLETED

    def test_from_str_fail(self) -> None:
        message = "Unknown status 'COMPLETE'"
        with pytest.raises(ValueError, match=re.escape(message)):
            BatchJobStatus.from_str("COMPLETE")

    @pytest.mark.parametrize(
        "status, is_terminal",
        [
            (BatchJobStatus.COMPLETED, True),
            (BatchJobStatus.FAILED, True),
            (BatchJobStatus.IN_PROGRESS, False),
            (BatchJobStatus.QUEUED, False),
        ],
    )
    def test_is_terminal(self, status: BatchJobStatus, is_terminal: bool) -> None:
        assert BatchJobStatus.is_terminal(status) == is_terminal
