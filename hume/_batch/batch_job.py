"""Batch job."""
import logging
from typing import TYPE_CHECKING

from hume._batch.batch_job_result import BatchJobResult
from hume._batch.batch_job_status import BatchJobStatus
from hume._common.retry_utils import retry, RetryIterError

if TYPE_CHECKING:
    from hume._batch.hume_batch_client import HumeBatchClient

logger = logging.getLogger(__name__)


class BatchJob:
    """Batch job."""

    def __init__(self, client: "HumeBatchClient", job_id: str):
        """Construct a BatchJob.

        Args:
            client (HumeBatchClient): HumeBatchClient instance.
            job_id (str): Job ID.
        """
        self._client = client
        self.id = job_id

    def get_status(self) -> BatchJobStatus:
        """Get the status of the job.

        Returns:
            BatchJobStatus: The status of the `BatchJob`.
        """
        return self.get_result().status

    def get_result(self) -> BatchJobResult:
        """Get the result of the BatchJob.

        Note that the result of a job may be fetched before the job has completed.
        You may want to use `job.await_complete()` which will wait for the job to
        reach a terminal state before returning the result.

        Returns:
            BatchJobResult: The result of the `BatchJob`.
        """
        return self._client.get_job_result(self.id)

    def await_complete(self, timeout: int = 300) -> BatchJobResult:
        """Block until the job has reached a terminal status.

        Args:
            timeout (int): Maximum time in seconds to await. If the timeout is reached
                before the job reaches a terminal state the job will continue to be processed,
                but a `HumeClientError` will be raised to the caller of `await_complete`.

        Raises:
            ValueError: If the timeout is not valid.

        Returns:
            BatchJobResult: The result of the `BatchJob`.
        """
        if timeout < 1:
            raise ValueError("timeout must be at least 1 second")

        return self._await_complete(timeout=timeout)

    # pylint: disable=unused-argument
    @retry()
    def _await_complete(self, timeout: int = 300) -> BatchJobResult:
        result = self._client.get_job_result(self.id)
        if not BatchJobStatus.is_terminal(result.status):
            raise RetryIterError
        return result

    def __repr__(self) -> str:
        """Get the string representation of the `BatchJob`.

        Returns:
            The the string representation of the `BatchJob`.
        """
        return f'Job(id="{self.id}")'
