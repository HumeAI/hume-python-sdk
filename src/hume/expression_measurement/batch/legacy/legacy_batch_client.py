"""Batch API client."""

from pathlib import Path
from typing import List, Optional, Union
import typing

from ...types.models import Models
from ...types.transcription import Transcription
from ...types.union_job import UnionJob
from ...types.union_predict_result import UnionPredictResult
from .batch_job import BatchJob

from ..client import AsyncBatchClient, BatchClient

# this is used as the default value for optional parameters
OMIT = typing.cast(typing.Any, ...)

class LegacyBatchClient:
    """Batch API client."""

    def __init__(self, *, batch_client: BatchClient):
        self._batch_client = batch_client

    def get_job(self, job_id: str) -> BatchJob:
        """Rehydrate a job based on a Job ID.

        Args:
            job_id (str): ID of the job to rehydrate.

        Returns:
            BatchJob: Job associated with the given ID.
        """
        return BatchJob(self, job_id)

    def submit_job(
        self,
        urls: List[str],
        configs: Optional[Models],
        transcription_config: Optional[Transcription] = None,
        callback_url: Optional[str] = None,
        notify: Optional[bool] = None,
        files: Optional[List[Union[str, Path]]] = None,
        text: Optional[List[str]] = None,
    ) -> BatchJob:
        """Submit a job for batch processing.

        Note: Only one config per model type should be passed.
            If more than one config is passed for a given model type, only the last config will be used.

        Args:
            urls (List[str]): List of URLs to media files to be processed.
            configs (Optional[Models]): List of model config objects to run on each media URL.
            transcription_config (Optional[Transcription]): A `Transcription` object.
            callback_url (Optional[str]): A URL to which a POST request will be sent upon job completion.
            notify (Optional[bool]): Wether an email notification should be sent upon job completion.
            files (Optional[List[Union[str, Path]]]): List of paths to files on the local disk to be processed.
            text (Optional[List[str]]): List of strings (raw text) to be processed.

        Returns:
            BatchJob: The `BatchJob` representing the batch computation.
        """
        request = self._batch_client.start_inference_job(models=configs, transcription=transcription_config, urls=urls, registry_files=files, text=text, callback_url=callback_url, notify=notify)
        return BatchJob(self, request.job_id)

    def get_job_details(self, job_id: str) -> UnionJob:
        """Get details for the batch job.

        Args:
            job_id (str): Job ID.

        Raises:
            HumeClientException: If the job details cannot be loaded.

        Returns:
            UnionJob: Batch job details.
        """
        return self._batch_client.get_job_details(job_id)

    def get_job_predictions(self, job_id: str) -> List[UnionPredictResult]:
        """Get a batch job's predictions.

        Args:
            job_id (str): Job ID.

        Raises:
            HumeClientException: If the job predictions cannot be loaded.

        Returns:
            List[UnionPredictResult]: Batch job predictions.
        """
        return self._batch_client.get_job_predictions(job_id)

    def download_job_artifacts(self, job_id: str, filepath: Union[str, Path]) -> None:
        """Download a batch job's artifacts as a zip file.

        Args:
            job_id (str): Job ID.
            filepath (Optional[Union[str, Path]]): Filepath where artifacts will be downloaded.

        Raises:
            HumeClientException: If the job artifacts cannot be loaded.

        Returns:
            None: Batch job artifacts are written to disk and not returned.
        """
        response = self._batch_client.get_job_artifacts(job_id)

        with Path(filepath).open("wb") as f:
            f.write(response.content)

class AsyncLegacyBatchClient:
    """Batch API client."""

    def __init__(self, *, batch_client: AsyncBatchClient):
        self._batch_client = batch_client

    def get_job(self, job_id: str) -> BatchJob:
        """Rehydrate a job based on a Job ID.

        Args:
            job_id (str): ID of the job to rehydrate.

        Returns:
            BatchJob: Job associated with the given ID.
        """
        return BatchJob(self, job_id)

    async def submit_job(
        self,
        urls: List[str],
        configs: Optional[Models],
        transcription_config: Optional[Transcription] = None,
        callback_url: Optional[str] = None,
        notify: Optional[bool] = None,
        files: Optional[List[Union[str, Path]]] = None,
        text: Optional[List[str]] = None,
    ) -> BatchJob:
        """Submit a job for batch processing.

        Note: Only one config per model type should be passed.
            If more than one config is passed for a given model type, only the last config will be used.

        Args:
            urls (List[str]): List of URLs to media files to be processed.
            configs (Optional[Models]): List of model config objects to run on each media URL.
            transcription_config (Optional[Transcription]): A `Transcription` object.
            callback_url (Optional[str]): A URL to which a POST request will be sent upon job completion.
            notify (Optional[bool]): Wether an email notification should be sent upon job completion.
            files (Optional[List[Union[str, Path]]]): List of paths to files on the local disk to be processed.
            text (Optional[List[str]]): List of strings (raw text) to be processed.

        Returns:
            BatchJob: The `BatchJob` representing the batch computation.
        """
        request = await self._batch_client.start_inference_job(models=configs, transcription=transcription_config, urls=urls, registry_files=files, text=text, callback_url=callback_url, notify=notify)
        return BatchJob(self, request.job_id)

    async def get_job_details(self, job_id: str) -> UnionJob:
        """Get details for the batch job.

        Args:
            job_id (str): Job ID.

        Raises:
            HumeClientException: If the job details cannot be loaded.

        Returns:
            UnionJob: Batch job details.
        """
        return await self._batch_client.get_job_details(job_id)

    async def get_job_predictions(self, job_id: str) -> List[UnionPredictResult]:
        """Get a batch job's predictions.

        Args:
            job_id (str): Job ID.

        Raises:
            HumeClientException: If the job predictions cannot be loaded.

        Returns:
            List[UnionPredictResult]: Batch job predictions.
        """
        return await self._batch_client.get_job_predictions(job_id)

    async def download_job_artifacts(self, job_id: str, filepath: Union[str, Path]) -> None:
        """Download a batch job's artifacts as a zip file.

        Args:
            job_id (str): Job ID.
            filepath (Optional[Union[str, Path]]): Filepath where artifacts will be downloaded.

        Raises:
            HumeClientException: If the job artifacts cannot be loaded.

        Returns:
            None: Batch job artifacts are written to disk and not returned.
        """
        response = await self._batch_client.get_job_artifacts(job_id)

        with Path(filepath).open("wb") as f:
            f.write(response.content)
