import logging
from typing import Optional, TYPE_CHECKING

from hume._clients.batch.batch_job_result import BatchJobResult
from hume._clients.batch.batch_job_status import BatchJobStatus
from hume._clients.common.retry_utils import retry, RetryIterError

if TYPE_CHECKING:
    from hume._clients.batch.hume_batch_client import HumeBatchClient

logger = logging.getLogger(__name__)


class BatchJob:

    def __init__(self, client: "HumeBatchClient", job_id: str):
        self.id = job_id
        self._client = client

    def await_complete(self, timeout: int = 300) -> Optional[BatchJobResult]:
        if timeout < 1:
            raise ValueError("timeout must be at least 1 second")

        return self._await_complete(timeout=timeout)

    @retry()
    def _await_complete(self, timeout: int = 300) -> BatchJobResult:
        result = self._client.get_job_result(self.id)
        if not BatchJobStatus.is_terminal(result.status):
            raise RetryIterError
        return result

    def __repr__(self) -> str:
        return f'Job(id="{self.id}")'
