from __future__ import annotations

import pytest
from hume import BatchJobState, BatchJobStatus


@pytest.mark.batch
class TestBatchJobState:
    def test_create(self) -> None:
        state = BatchJobState(
            status=BatchJobStatus.COMPLETED,
            created_timestamp_ms=1,
            started_timestamp_ms=2,
            ended_timestamp_ms=3,
        )
        assert state.status == BatchJobStatus.COMPLETED
        assert state.created_timestamp_ms == 1
        assert state.started_timestamp_ms == 2
        assert state.ended_timestamp_ms == 3
