"""Batch job state."""

from __future__ import annotations

from dataclasses import dataclass

from hume.legacy._measurement.batch.batch_job_status import BatchJobStatus


@dataclass
class BatchJobState:
    """Batch job state.

    Args:
        status (BatchJobStatus): Status of the batch job.
        created_timestamp_ms (int | None): Time when job was created.
        started_timestamp_ms (int | None): Time when job started.
        ended_timestamp_ms (int | None): Time when job ended.
    """

    status: BatchJobStatus
    created_timestamp_ms: int | None
    started_timestamp_ms: int | None
    ended_timestamp_ms: int | None
