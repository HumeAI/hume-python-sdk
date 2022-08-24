"""Batch job."""
import logging
from typing import TYPE_CHECKING

from hume.batch.batch_job_result import BatchJobResult
from hume.batch.batch_job_status import BatchJobStatus
from hume.common.retry_utils import retry, RetryIterError

if TYPE_CHECKING:
    from hume.batch.hume_batch_client import HumeBatchClient

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

    def await_complete(self, timeout: int = 300) -> BatchJobResult:
        """Block until the job has reached a terminal status.

        Args:
            timeout (int): Maximum time in seconds to await before failing.
                Will fail with `HumeClientError` if timeout is reached.

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
