"""Batch job."""
import json
from pathlib import Path
from typing import TYPE_CHECKING, Any, Union

from hume._batch.batch_job_details import BatchJobDetails
from hume._batch.batch_job_status import BatchJobStatus
from hume._common.retry_utils import RetryIterError, retry
from hume.error.hume_client_exception import HumeClientException

if TYPE_CHECKING:
    from hume._batch.hume_batch_client import HumeBatchClient


class BatchJob:
    """Batch job."""

    TIMEOUT_MESSAGE = (
        "Connection to API has been terminated after {}s, but your job will continue to run. "
        "Get a reference to your job with `client.get_job('{}')` at any time."
    )

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

    def await_complete(self, timeout: int = 300, raise_on_failed: bool = False) -> BatchJobDetails:
        """Block until the job has reached a terminal status.

        Args:
            timeout (int): Maximum time in seconds to await. If the timeout is reached
                before the job reaches a terminal state the job will continue to be processed,
                but a `HumeClientException` will be raised to the caller of `await_complete`.
            raise_on_failed (bool): If set to True and job fails an exception will be raised.

        Raises:
            ValueError: If the timeout is not valid.
            HumeClientException: If the `BatchJob` has not reached a terminal state within
                the specified timeout. Also can be raised if `raise_on_failed` is set and
                the job reaches a `FAILED` terminal state.

        Returns:
            BatchJobDetails: Details for the `BatchJob`.
        """
        if timeout < 1:
            raise ValueError("timeout must be at least 1 second")

        # pylint: disable=unused-argument
        @retry(timeout_message=self.TIMEOUT_MESSAGE.format(timeout, self.id))
        def _await_complete(timeout: int = timeout) -> BatchJobDetails:
            details = self._client.get_job_details(self.id)
            if not BatchJobStatus.is_terminal(details.state.status):
                raise RetryIterError
            if raise_on_failed and details.state.status == BatchJobStatus.FAILED:
                raise HumeClientException(f"BatchJob {self.id} failed.")
            return details

        return _await_complete(timeout=timeout)

    def __repr__(self) -> str:
        """Get the string representation of the `BatchJob`.

        Returns:
            The the string representation of the `BatchJob`.
        """
        return f'Job(id="{self.id}")'
