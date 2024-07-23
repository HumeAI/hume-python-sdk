"""Batch API client."""

from __future__ import annotations

import json
from collections.abc import Iterable
from pathlib import Path
from typing import Any, Optional, Union

from hume.legacy._common.client_base import ClientBase
from hume.legacy._common.utilities.config_utilities import serialize_configs
from hume.legacy._measurement.batch.batch_job import BatchJob
from hume.legacy._measurement.batch.batch_job_details import BatchJobDetails
from hume.legacy._measurement.batch.transcription_config import TranscriptionConfig
from hume.legacy.error.hume_client_exception import HumeClientException
from hume.legacy.models.config.model_config_base import ModelConfigBase


class HumeBatchClient(ClientBase):
    """Batch API client.

    Example:
        ```python
        from hume import HumeBatchClient
        from hume.models.config import FaceConfig
        from hume.models.config import ProsodyConfig

        client = HumeBatchClient("<your-api-key>")
        urls = ["https://storage.googleapis.com/hume-test-data/video/armisen-clip.mp4"]
        configs = [FaceConfig(identify_faces=True), ProsodyConfig()]
        job = client.submit_job(urls, configs)

        print(job)
        print("Running...")

        job.await_complete()
        job.download_predictions("predictions.json")
        print("Predictions downloaded to predictions.json")

        job.download_artifacts("artifacts.zip")
        print("Artifacts downloaded to artifacts.zip")
        ```
    """

    def __init__(
        self,
        api_key: str,
        *args: Any,
        timeout: int = 10,
        **kwargs: Any,
    ):
        """Construct a HumeBatchClient.

        Args:
            api_key (str): Hume API key.
            timeout (int): Time in seconds before canceling long-running Hume API requests.
        """
        super().__init__(api_key, http_timeout=timeout, *args, **kwargs)

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
        urls: list[str],
        configs: Iterable[ModelConfigBase],
        transcription_config: TranscriptionConfig | None = None,
        callback_url: str | None = None,
        notify: bool | None = None,
        files: list[Path | str] | None = None,
        filebytes: Optional[list[tuple[str, bytes]]] = None,
        text: list[str] | None = None,
    ) -> BatchJob:
        """Submit a job for batch processing.

        Note: Only one config per model type should be passed.
            If more than one config is passed for a given model type, only the last config will be used.

        Args:
            urls (list[str]): List of URLs to media files to be processed.
            configs (Iterable[ModelConfigBase]): Iterable of model config objects to run on each media URL.
            transcription_config (TranscriptionConfig | None): A `TranscriptionConfig` object.
            callback_url (str | None): A URL to which a POST request will be sent upon job completion.
            notify (bool | None): Wether an email notification should be sent upon job completion.
            files (list[Path | str] | None): List of paths to files on the local disk to be processed.
            filebytes (list[tuple[str, bytes]] | None): List of file bytes (raw file data) to be processed.
            text (list[str] | None): List of strings (raw text) to be processed.

        Returns:
            BatchJob: The `BatchJob` representing the batch computation.
        """
        request = self._construct_request(configs, urls, text, transcription_config, callback_url, notify)
        return self._submit_job(request, files, filebytes)

    def get_job_details(self, job_id: str) -> BatchJobDetails:
        """Get details for the batch job.

        Args:
            job_id (str): Job ID.

        Raises:
            HumeClientException: If the job details cannot be loaded.

        Returns:
            BatchJobDetails: Batch job details.
        """
        endpoint = self._build_endpoint("batch", f"jobs/{job_id}")
        response = self._http_client.get(endpoint, headers=self._get_client_headers())

        try:
            body = response.json()
        except json.JSONDecodeError:
            # pylint: disable=raise-missing-from
            raise HumeClientException("Unexpected error when getting job details")

        if "message" in body and body["message"] == "job not found":
            raise HumeClientException(f"Could not find a job with ID {job_id}")

        return BatchJobDetails.from_response(body)

    def get_job_predictions(self, job_id: str) -> Any:
        """Get a batch job's predictions.

        Args:
            job_id (str): Job ID.

        Raises:
            HumeClientException: If the job predictions cannot be loaded.

        Returns:
            Any: Batch job predictions.
        """
        endpoint = self._build_endpoint("batch", f"jobs/{job_id}/predictions")
        response = self._http_client.get(endpoint, headers=self._get_client_headers())

        try:
            body = response.json()
        except json.JSONDecodeError:
            # pylint: disable=raise-missing-from
            raise HumeClientException("Unexpected error when getting job predictions")

        if "message" in body and body["message"] == "job not found":
            raise HumeClientException(f"Could not find a job with ID {job_id}")

        return body

    def download_job_artifacts(self, job_id: str, filepath: Path | str) -> None:
        """Download a batch job's artifacts as a zip file.

        Args:
            job_id (str): Job ID.
            filepath (Path | str | None): Filepath where artifacts will be downloaded.

        Raises:
            HumeClientException: If the job artifacts cannot be loaded.

        Returns:
            Any: Batch job artifacts.
        """
        endpoint = self._build_endpoint("batch", f"jobs/{job_id}/artifacts")
        response = self._http_client.get(endpoint, headers=self._get_client_headers())

        with Path(filepath).open("wb") as f:
            f.write(response.content)

    @classmethod
    def _construct_request(
        cls,
        configs: Iterable[ModelConfigBase],
        urls: list[str],
        text: list[str] | None,
        transcription_config: TranscriptionConfig | None,
        callback_url: str | None,
        notify: bool | None,
    ) -> dict[str, Any]:
        request: dict[str, Any] = {
            "urls": urls,
            "models": serialize_configs(configs),
        }
        if text is not None:
            request["text"] = text
        if transcription_config is not None:
            request["transcription"] = transcription_config.to_dict()
        if callback_url is not None:
            request["callback_url"] = callback_url
        if notify is not None:
            request["notify"] = notify
        return request

    def _submit_job(
        self,
        request_body: Any,
        filepaths: list[Path | str] | None,
        filebytes: Optional[list[tuple[str, bytes]]],
    ) -> BatchJob:
        """Start a job for batch processing by passing a JSON request body.

        This request body should match the request body used by the batch API,
        including both the list of URLs and the models configuration.

        Args:
            request_body (Any): JSON request body to be passed to the batch API.
            filepaths (list[Path | str] | None): List of paths to files on the local disk to be processed.
            filebytes (list[tuple[str, bytes]]] | None): List of bytes (raw file data) to be processed.

        Raises:
            HumeClientException: If the batch job fails to start.

        Returns:
            BatchJob: A `BatchJob` that wraps the batch computation.
        """
        endpoint = self._build_endpoint("batch", "jobs")

        if filepaths is None and filebytes is None:
            response = self._http_client.post(
                endpoint,
                json=request_body,
                headers=self._get_client_headers(),
            )
        else:
            form_data = self._get_multipart_form_data(request_body, filepaths, filebytes)
            response = self._http_client.post(
                endpoint,
                headers=self._get_client_headers(),
                files=form_data,
            )

        try:
            body = response.json()
        except json.decoder.JSONDecodeError:
            # pylint: disable=raise-missing-from
            raise HumeClientException(f"Failed batch request: {response.text}")

        if "job_id" not in body:
            if "fault" in body and "faultstring" in body["fault"]:
                fault = body["fault"]
                fault_string = fault["faultstring"]
                if "detail" in fault and "errorcode" in fault["detail"]:
                    detail = fault["detail"]
                    error_code = detail["errorcode"]
                    if "InvalidApiKey" in error_code:
                        raise HumeClientException("HumeBatchClient initialized with invalid API key.")
                    raise HumeClientException(f"Could not start batch job: {error_code}: {fault_string}")
                raise HumeClientException(f"Could not start batch job: {fault_string}")
            raise HumeClientException(f"Unexpected error when starting batch job: {body}")

        return BatchJob(self, body["job_id"])

    def _get_multipart_form_data(
        self,
        request_body: Any,
        filepaths: Optional[Iterable[Union[str, Path]]],
        filebytes: Optional[Iterable[tuple[str, bytes]]],
    ) -> list[tuple[str, Union[bytes, tuple[str, bytes]]]]:
        """Convert a list of filepaths and/or file bytes into a list of multipart form data.

        Multipart form data allows the client to attach files to the POST request,
        including both the raw file bytes and the filename.

        Args:
            request_body (Any): JSON request body to be passed to the batch API.
            filepaths (list[Path | str] | None): List of paths to files on the local disk to be processed.
            filebytes (list[str | bytes] | None): List of bytes (raw file data) to be processed.

        Returns:
            list[tuple[str, bytes | tuple[str, bytes]]]: A list of tuples representing
                the multipart form data for the POST request.
        """
        form_data: list[tuple[str, Union[bytes, tuple[str, bytes]]]] = []
        if filepaths is not None:
            for filepath in filepaths:
                path = Path(filepath)
                post_file = ("file", (path.name, path.read_bytes()))
                form_data.append(post_file)
        if filebytes is not None:
            for filebyte in filebytes:
                post_file = ("file", filebyte)
                form_data.append(post_file)

        form_data.append(("json", json.dumps(request_body).encode("utf-8")))
        return form_data
