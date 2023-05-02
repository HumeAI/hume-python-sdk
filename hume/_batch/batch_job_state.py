"""Batch job state."""
from dataclasses import dataclass
from datetime import datetime
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

    def get_run_time_ms(self) -> Optional[int]:
        """Get the total time in milliseconds it took for the job to run if the job is in a terminal state.

        Returns:
            Optional[int]: Time in milliseconds it took for the job to run. If the job is not in a terminal
                state then `None` is returned.
        """
        if self.started_timestamp_ms is not None and self.ended_timestamp_ms is not None:
            return self.ended_timestamp_ms - self.started_timestamp_ms
        return None

    def get_created_time(self) -> Optional[datetime]:
        """Get the time the job was created.

        Returns:
            Optional[datetime]: Datetime when the job was created. If the job has not started
                then `None` is returned.
        """
        if self.created_timestamp_ms is None:
            return None
        return datetime.utcfromtimestamp(self.created_timestamp_ms / 1000)

    def get_started_time(self) -> Optional[datetime]:
        """Get the time the job started running.

        Returns:
            Optional[datetime]: Datetime when the job started running. If the job has not started
                then `None` is returned.
        """
        if self.started_timestamp_ms is None:
            return None
        return datetime.utcfromtimestamp(self.started_timestamp_ms / 1000)

    def get_ended_time(self) -> Optional[datetime]:
        """Get the time the job stopped running if the job is in a terminal state.

        Returns:
            Optional[datetime]: Datetime when the job started running. If the job is not in a terminal
                state then `None` is returned.
        """
        if self.ended_timestamp_ms is None:
            return None
        return datetime.utcfromtimestamp(self.ended_timestamp_ms / 1000)
