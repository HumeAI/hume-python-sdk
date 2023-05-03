"""Batch job state."""
from dataclasses import dataclass
from typing import Optional

from hume._batch.batch_job_status import BatchJobStatus


@dataclass
class BatchJobState:
    """Batch job state.

    Args:
        status (BatchJobStatus): Status of the batch job.
        created_timestamp_ms (Optional[int]): Time when job was created.
        started_timestamp_ms (Optional[int]): Time when job started.
        ended_timestamp_ms (Optional[int]): Time when job ended.
    """

    status: BatchJobStatus
    created_timestamp_ms: Optional[int]
    started_timestamp_ms: Optional[int]
    ended_timestamp_ms: Optional[int]
