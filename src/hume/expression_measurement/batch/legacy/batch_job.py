"""Batch job."""

import json
from pathlib import Path
from typing import TYPE_CHECKING, Any, List, Union

from hume.core import jsonable_encoder
from hume.custom_models.types.union_predict_result import UnionPredictResult

from .retry_utilities import RetryIterError, retry
from ...types.status import Status
from ...types.union_job import UnionJob
from ....core.api_error import ApiError

if TYPE_CHECKING:
    from .legacy_batch_client import LegacyBatchClient, AsyncLegacyBatchClient


class BatchJob:
    """Batch job."""

    TIMEOUT_MESSAGE = (
        "Connection to API has been terminated after {}s, but your job will continue to run. "
        "Get a reference to your job with `client.get_job('{}')` at any time."
    )

    def __init__(self, client: "LegacyBatchClient", job_id: str):
        """Construct a BatchJob.

        Args:
            client (HumeBatchClient): HumeBatchClient instance.
            job_id (str): Job ID.
        """
        self._client = client
        self.id = job_id

    def get_status(self) -> Status:
        """Get the status of the job.

        Returns:
            Status: The status of the `BatchJob`.
        """
        return self.get_details().state.status

    def get_predictions(self) -> List[UnionPredictResult]:
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
            json.dump(jsonable_encoder(predictions), f)

    def download_artifacts(self, filepath: Union[str, Path]) -> None:
        """Download `BatchJob` artifacts zip file.

        Args:
            filepath (Optional[Union[str, Path]]): Filepath where artifacts will be downloaded.
        """
        self._client.download_job_artifacts(self.id, filepath)

    def get_details(self) -> UnionJob:
        """Get details for the BatchJob.

        Note that the details for a job may be fetched before the job has completed.
        You may want to use `job.await_complete()` which will wait for the job to
        reach a terminal state before returning.

        Returns:
            UnionJob: Details for the `BatchJob`.
        """
        return self._client.get_job_details(self.id)

    def await_complete(self, timeout: int = 300, raise_on_failed: bool = False) -> UnionJob:
        """Block until the job has reached a terminal status.

        Args:
            timeout (int): Maximum time in seconds to await. If the timeout is reached
                before the job reaches a terminal state the job will continue to be processed,
                but a `ApiError` will be raised to the caller of `await_complete`.
            raise_on_failed (bool): If set to True and job fails an exception will be raised.

        Raises:
            ValueError: If the timeout is not valid.
            ApiError: If the `BatchJob` has not reached a terminal state within
                the specified timeout. Also can be raised if `raise_on_failed` is set and
                the job reaches a `FAILED` terminal state.

        Returns:
            UnionJob: Details for the `BatchJob`.
        """
        if timeout < 1:
            raise ValueError("timeout must be at least 1 second")

        # pylint: disable=unused-argument
        @retry(timeout_message=self.TIMEOUT_MESSAGE.format(timeout, self.id))
        def _await_complete(timeout: int = timeout) -> UnionJob:
            details = self._client.get_job_details(self.id)
            if details.state.status != "COMPLETED" and details.state.status != "FAILED":
                raise RetryIterError
            if raise_on_failed and details.state.status == "FAILED":
                raise ApiError(body=f"BatchJob {self.id} failed.")
            return details

        return _await_complete(timeout=timeout)

    def __repr__(self) -> str:
        """Get the string representation of the `BatchJob`.

        Returns:
            The the string representation of the `BatchJob`.
        """
        return f'Job(id="{self.id}")'

class AsyncBatchJob:
    """Batch job."""

    TIMEOUT_MESSAGE = (
        "Connection to API has been terminated after {}s, but your job will continue to run. "
        "Get a reference to your job with `client.get_job('{}')` at any time."
    )

    def __init__(self, client: "AsyncLegacyBatchClient", job_id: str):
        """Construct a BatchJob.

        Args:
            client (HumeBatchClient): HumeBatchClient instance.
            job_id (str): Job ID.
        """
        self._client = client
        self.id = job_id

    async def get_status(self) -> Status:
        """Get the status of the job.

        Returns:
            Status: The status of the `BatchJob`.
        """
        return (await self.get_details()).state.status

    async def get_predictions(self) -> Any:
        """Get `BatchJob` predictions.

        Returns:
            Any: Predictions for the `BatchJob`.
        """
        return await self._client.get_job_predictions(self.id)

    async def download_predictions(self, filepath: Union[str, Path]) -> None:
        """Download `BatchJob` predictions file.

        Args:
            filepath (Union[str, Path]): Filepath where predictions will be downloaded.
        """
        predictions = await self.get_predictions()
        with Path(filepath).open("w") as f:
            json.dump(predictions, f)

    async def download_artifacts(self, filepath: Union[str, Path]) -> None:
        """Download `BatchJob` artifacts zip file.

        Args:
            filepath (Optional[Union[str, Path]]): Filepath where artifacts will be downloaded.
        """
        await self._client.download_job_artifacts(self.id, filepath)

    async def get_details(self) -> UnionJob:
        """Get details for the BatchJob.

        Note that the details for a job may be fetched before the job has completed.
        You may want to use `job.await_complete()` which will wait for the job to
        reach a terminal state before returning.

        Returns:
            UnionJob: Details for the `BatchJob`.
        """
        return await self._client.get_job_details(self.id)

    async def await_complete(self, timeout: int = 300, raise_on_failed: bool = False) -> UnionJob:
        """Block until the job has reached a terminal status.

        Args:
            timeout (int): Maximum time in seconds to await. If the timeout is reached
                before the job reaches a terminal state the job will continue to be processed,
                but a `ApiError` will be raised to the caller of `await_complete`.
            raise_on_failed (bool): If set to True and job fails an exception will be raised.

        Raises:
            ValueError: If the timeout is not valid.
            ApiError: If the `BatchJob` has not reached a terminal state within
                the specified timeout. Also can be raised if `raise_on_failed` is set and
                the job reaches a `FAILED` terminal state.

        Returns:
            UnionJob: Details for the `BatchJob`.
        """
        if timeout < 1:
            raise ValueError("timeout must be at least 1 second")

        # pylint: disable=unused-argument
        @retry(timeout_message=self.TIMEOUT_MESSAGE.format(timeout, self.id))
        async def _await_complete(timeout: int = timeout) -> UnionJob:
            details = await self._client.get_job_details(self.id)
            if details.state.status != "COMPLETED" and details.state.status != "FAILED":
                raise RetryIterError
            if raise_on_failed and details.state.status == "FAILED":
                raise ApiError(body=f"BatchJob {self.id} failed.")
            return details

        return await _await_complete(timeout=timeout)

    def __repr__(self) -> str:
        """Get the string representation of the `BatchJob`.

        Returns:
            The the string representation of the `BatchJob`.
        """
        return f'Job(id="{self.id}")'
