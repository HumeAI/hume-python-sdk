"""Batch API client."""
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

from requests import Session

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
        self._timeout = timeout
        self._session = Session()
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
        notify: Optional[bool] = None,
        files: Optional[List[Union[str, Path]]] = None,
        text: Optional[List[str]] = None,
    ) -> BatchJob:
        """Submit a job for batch processing.

        Note: Only one config per model type should be passed.
            If more than one config is passed for a given model type, only the last config will be used.

        Args:
            urls (List[str]): List of URLs to media files to be processed.
            configs (List[ModelConfigBase]): List of model config objects to run on each media URL.
            transcription_config (Optional[TranscriptionConfig]): A `TranscriptionConfig` object.
            callback_url (Optional[str]): A URL to which a POST request will be sent upon job completion.
            notify (Optional[bool]): Wether an email notification should be sent upon job completion.
            files (Optional[List[Union[str, Path]]]): List of paths to files on the local disk to be processed.
            text (Optional[List[str]]): List of strings (raw text) to be processed.

        Returns:
            BatchJob: The `BatchJob` representing the batch computation.
        """
        request = self._construct_request(configs, urls, text, transcription_config, callback_url, notify)
        return self._submit_job(request, files)

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
        response = self._session.get(
            endpoint,
            timeout=self._timeout,
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
        response = self._session.get(
            endpoint,
            timeout=self._timeout,
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
        response = self._session.get(
            endpoint,
            timeout=self._timeout,
            headers=self._get_client_headers(),
        )

        with Path(filepath).open("wb") as f:
            f.write(response.content)

    @classmethod
    def _construct_request(
        cls,
        configs: List[ModelConfigBase],
        urls: List[str],
        text: Optional[List[str]],
        transcription_config: Optional[TranscriptionConfig],
        callback_url: Optional[str],
        notify: Optional[bool],
    ) -> Dict[str, Any]:
        request: Dict[str, Any] = {
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
        filepaths: Optional[List[Union[str, Path]]],
    ) -> BatchJob:
        """Start a job for batch processing by passing a JSON request body.

        This request body should match the request body used by the batch API,
        including both the list of URLs and the models configuration.

        Args:
            request_body (Any): JSON request body to be passed to the batch API.
            filepaths (Optional[List[Union[str, Path]]]): List of paths to files on the local disk to be processed.

        Raises:
            HumeClientException: If the batch job fails to start.

        Returns:
            BatchJob: A `BatchJob` that wraps the batch computation.
        """
        endpoint = self._construct_endpoint("jobs")

        if filepaths is None:
            response = self._session.post(
                endpoint,
                json=request_body,
                timeout=self._timeout,
                headers=self._get_client_headers(),
            )
        else:
            form_data = self._get_multipart_form_data(request_body, filepaths)
            response = self._session.post(
                endpoint,
                timeout=self._timeout,
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
        filepaths: List[Union[str, Path]],
    ) -> List[Tuple[str, Union[bytes, Tuple[str, bytes]]]]:
        """Convert a list of filepaths into a list of multipart form data.

        Multipart form data allows the client to attach files to the POST request,
        including both the raw file bytes and the filename.

        Args:
            request_body (Any): JSON request body to be passed to the batch API.
            filepaths (List[Union[str, Path]]): List of paths to files on the local disk to be processed.

        Returns:
            List[Tuple[str, Union[bytes, Tuple[str, bytes]]]]: A list of tuples representing
                the multipart form data for the POST request.
        """
        form_data: List[Tuple[str, Union[bytes, Tuple[str, bytes]]]] = []
        for filepath in filepaths:
            path = Path(filepath)
            post_file = ("file", (path.name, path.read_bytes()))
            form_data.append(post_file)

        form_data.append(("json", json.dumps(request_body).encode("utf-8")))
        return form_data
