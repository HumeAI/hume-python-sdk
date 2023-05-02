"""Batch job."""
import json
from pathlib import Path
from typing import TYPE_CHECKING, Any, Union

from hume._batch.batch_job_details import BatchJobDetails
from hume._batch.batch_job_status import BatchJobStatus
from hume._common.retry_utils import retry, RetryIterError

if TYPE_CHECKING:
    from hume._batch.hume_batch_client import HumeBatchClient


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
        return self.get_details().state.status

    def get_predictions(self) -> Any:
        """Get `BatchJob` predictions.

        Returns:
            Any: Predictions for the `BatchJob`.
        """
        return self._client.get_job_predictions(self.id)

    def download_predictions(self, filepath: Union[str, Path]) -> None:
        """Download `BatchJob` predictions file.

        Args:
            filepath (Union[str, Path]): Filepath where predictions will be downloaded.
        """
        predictions = self.get_predictions()
        with Path(filepath).open("w") as f:
            json.dump(predictions, f)

    def download_artifacts(self, filepath: Union[str, Path]) -> None:
        """Download `BatchJob` artifacts zip file.

        Args:
            filepath (Optional[Union[str, Path]]): Filepath where artifacts will be downloaded.
        """
        self._client.download_job_artifacts(self.id, filepath)

    def get_details(self) -> BatchJobDetails:
        """Get details for the BatchJob.

        Note that the details for a job may be fetched before the job has completed.
        You may want to use `job.await_complete()` which will wait for the job to
        reach a terminal state before returning.

        Returns:
            BatchJobDetails: Details for the `BatchJob`.
        """
        return self._client.get_job_details(self.id)

    def await_complete(self, timeout: int = 300) -> BatchJobDetails:
        """Block until the job has reached a terminal status.

        Args:
            timeout (int): Maximum time in seconds to await. If the timeout is reached
                before the job reaches a terminal state the job will continue to be processed,
                but a `HumeClientException` will be raised to the caller of `await_complete`.

        Raises:
            ValueError: If the timeout is not valid.

        Returns:
            BatchJobDetails: Details for the `BatchJob`.
        """
        if timeout < 1:
            raise ValueError("timeout must be at least 1 second")

        return self._await_complete(timeout=timeout)

    # pylint: disable=unused-argument
    @retry()
    def _await_complete(self, timeout: int = 300) -> BatchJobDetails:
        details = self._client.get_job_details(self.id)
        if not BatchJobStatus.is_terminal(details.state.status):
            raise RetryIterError
        return details

    def __repr__(self) -> str:
        """Get the string representation of the `BatchJob`.

        Returns:
            The the string representation of the `BatchJob`.
        """
        return f'Job(id="{self.id}")'
