"""Batch API client."""
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import requests

from hume._batch.batch_job import BatchJob
from hume._batch.batch_job_details import BatchJobDetails
from hume._batch.transcription_config import TranscriptionConfig
from hume._common.api_type import ApiType
from hume._common.client_base import ClientBase
from hume._common.config_utils import serialize_configs
from hume.error.hume_client_exception import HumeClientException
from hume.models.config.model_config_base import ModelConfigBase


class HumeBatchClient(ClientBase):
    """Batch API client.

    Example:
        ```python
        from hume import HumeBatchClient
        from hume.models.config import FaceConfig

        client = HumeBatchClient("<your-api-key>")
        urls = ["https://tinyurl.com/hume-img"]
        config = FaceConfig(identify_faces=True)
        job = client.submit_job(urls, [config])

        print(job)
        print("Running...")

        job.await_complete()
        job.download_predictions("predictions.json")
        print("Predictions downloaded to predictions.json")

        job.download_artifacts("artifacts.zip")
        print("Artifacts downloaded to artifacts.zip")
        ```
    """

    _DEFAULT_API_TIMEOUT = 10

    def __init__(self, api_key: str, *args: Any, **kwargs: Any):
        """Construct a HumeBatchClient.

        Args:
            api_key (str): Hume API key.
        """
        super().__init__(api_key, *args, **kwargs)

    @classmethod
    def get_api_type(cls) -> ApiType:
        """Get the ApiType of the client.

        Returns:
            ApiType: API type of the client.
        """
        return ApiType.BATCH

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
        configs: List[ModelConfigBase],
        transcription_config: Optional[TranscriptionConfig] = None,
        callback_url: Optional[str] = None,
    ) -> BatchJob:
        """Submit a job for batch processing.

        Note: Only one config per model type should be passed.
            If more than one config is passed for a given model type, only the last config will be used.

        Args:
            urls (List[str]): List of URLs to media files to be processed.
            configs (List[ModelConfigBase]): List of model config objects to run on each media URL.
            transcription_config (Optional[TranscriptionConfig]): A `TranscriptionConfig` object.
            callback_url (Optional[str]): A URL to which a POST request will be sent upon job completion.

        Returns:
            BatchJob: The `BatchJob` representing the batch computation.
        """
        request = self._construct_request(configs, urls, transcription_config, callback_url)
        return self._submit_job_from_request(request)

    def get_job_details(self, job_id: str) -> BatchJobDetails:
        """Get details for the batch job.

        Args:
            job_id (str): Job ID.

        Raises:
            HumeClientException: If the job details cannot be loaded.

        Returns:
            BatchJobDetails: Batch job details.
        """
        endpoint = self._construct_endpoint(f"jobs/{job_id}")
        response = requests.get(
            endpoint,
            timeout=self._DEFAULT_API_TIMEOUT,
            headers=self._get_client_headers(),
        )

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
        endpoint = self._construct_endpoint(f"jobs/{job_id}/predictions")
        response = requests.get(
            endpoint,
            timeout=self._DEFAULT_API_TIMEOUT,
            headers=self._get_client_headers(),
        )

        try:
            body = response.json()
        except json.JSONDecodeError:
            # pylint: disable=raise-missing-from
            raise HumeClientException("Unexpected error when getting job predictions")

        if "message" in body and body["message"] == "job not found":
            raise HumeClientException(f"Could not find a job with ID {job_id}")

        return body

    def download_job_artifacts(self, job_id: str, filepath: Union[str, Path]) -> None:
        """Download a batch job's artifacts as a zip file.

        Args:
            job_id (str): Job ID.
            filepath (Optional[Union[str, Path]]): Filepath where artifacts will be downloaded.

        Raises:
            HumeClientException: If the job artifacts cannot be loaded.

        Returns:
            Any: Batch job artifacts.
        """
        endpoint = self._construct_endpoint(f"jobs/{job_id}/artifacts")
        response = requests.get(
            endpoint,
            timeout=self._DEFAULT_API_TIMEOUT,
            headers=self._get_client_headers(),
        )

        with Path(filepath).open("wb") as f:
            f.write(response.content)

    @classmethod
    def _construct_request(
        cls,
        configs: List[ModelConfigBase],
        urls: List[str],
        transcription_config: Optional[TranscriptionConfig],
        callback_url: Optional[str],
    ) -> Dict[str, Any]:
        request = {
            "urls": urls,
            "models": serialize_configs(configs),
        }
        if transcription_config is not None:
            request["transcription"] = transcription_config.to_dict()
        if callback_url is not None:
            request["callback_url"] = callback_url
        return request

    def _submit_job_from_request(self, request_body: Any) -> BatchJob:
        """Start a job for batch processing by passing a JSON request body.

        This request body should match the request body used by the batch API,
        including both the list of URLs and the models configuration.

        Args:
            request_body (Any): JSON request body to be passed to the batch API.

        Raises:
            HumeClientException: If the batch job fails to start.

        Returns:
            BatchJob: A `BatchJob` that wraps the batch computation.
        """
        endpoint = self._construct_endpoint("jobs")
        response = requests.post(
            endpoint,
            json=request_body,
            timeout=self._DEFAULT_API_TIMEOUT,
            headers=self._get_client_headers(),
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
