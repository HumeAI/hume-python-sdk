"""Batch API client."""

from pathlib import Path
from typing import List, Optional, Union
import typing

from ...types.inference_base_request import InferenceBaseRequest
from ...types.models import Models
from ...types.transcription import Transcription
from ...types.union_job import UnionJob
from ...types.union_predict_result import UnionPredictResult
from .batch_job import AsyncBatchJob, BatchJob
from .... import core
from ..client import AsyncBatchClient, BatchClient

# this is used as the default value for optional parameters
OMIT = typing.cast(typing.Any, ...)

    
def _get_multipart_form_data(filepaths: List[Union[str, Path]]) -> List[core.File]:
    """Convert a list of filepaths into a list of multipart form data.

    Multipart form data allows the client to attach files to the POST request,
    including both the raw file bytes and the filename.

    Args:
        filepaths (List[Union[str, Path]]): List of paths to files on the local disk to be processed.

    Returns:
        List[core.File]: A list of tuples representing
            the multipart form data for the POST request.
    """
    form_data: List[core.File] = []
    for filepath in filepaths:
        path = Path(filepath)
        form_data.append((path.name, path.read_bytes()))

    return form_data

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
        if files is not None:
            form_data = _get_multipart_form_data(files)
            request = self._batch_client.start_inference_job_from_local_file(
                file=form_data,
                json=InferenceBaseRequest(
                    models=configs,
                    transcription=transcription_config,
                    urls=urls,
                    text=text,
                    callback_url=callback_url,
                    notify=notify
                )
            )
        else:
            request = self._batch_client.start_inference_job(models=configs, transcription=transcription_config, urls=urls, text=text, callback_url=callback_url, notify=notify)
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
            for chunk in response:
                f.write(chunk)

class AsyncLegacyBatchClient:
    """Batch API client."""

    def __init__(self, *, batch_client: AsyncBatchClient):
        self._batch_client = batch_client

    def get_job(self, job_id: str) -> AsyncBatchJob:
        """Rehydrate a job based on a Job ID.

        Args:
            job_id (str): ID of the job to rehydrate.

        Returns:
            BatchJob: Job associated with the given ID.
        """
        return AsyncBatchJob(self, job_id)

    async def submit_job(
        self,
        urls: List[str],
        configs: Optional[Models],
        transcription_config: Optional[Transcription] = None,
        callback_url: Optional[str] = None,
        notify: Optional[bool] = None,
        files: Optional[List[Union[str, Path]]] = None,
        text: Optional[List[str]] = None,
    ) -> AsyncBatchJob:
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
        if files is not None:
            form_data = _get_multipart_form_data(files)
            request = await self._batch_client.start_inference_job_from_local_file(
                file=form_data,
                json=InferenceBaseRequest(
                    models=configs,
                    transcription=transcription_config,
                    urls=urls,
                    text=text,
                    callback_url=callback_url,
                    notify=notify
                )
            )
        else:
            request = await self._batch_client.start_inference_job(models=configs, transcription=transcription_config, urls=urls, text=text, callback_url=callback_url, notify=notify)
        return AsyncBatchJob(self, request.job_id)

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
        response = self._batch_client.get_job_artifacts(job_id)

        with Path(filepath).open("wb") as f:
            async for chunk in response:
                f.write(chunk)
