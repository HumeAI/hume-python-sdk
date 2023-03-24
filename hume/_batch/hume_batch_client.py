"""Batch API client."""
import json
import logging
from typing import Any, Dict, List, Optional

import requests

from hume._batch.batch_job import BatchJob
from hume._batch.batch_job_result import BatchJobResult
from hume._common.config import BurstConfig, FaceConfig, LanguageConfig, ProsodyConfig, JobConfigBase
from hume._common.api_type import ApiType
from hume._common.client_base import ClientBase
from hume._common.hume_client_error import HumeClientError

logger = logging.getLogger(__name__)


class HumeBatchClient(ClientBase):
    """Batch API client.

    Example:
        ```python
        from hume import HumeBatchClient

        client = HumeBatchClient("<your-api-key>")
        job = client.submit_face(["<your-image-url>"])

        print(job)
        print("Running...")

        result = job.await_complete()
        result.download_predictions("predictions.json")

        print("Predictions downloaded!")
        ```
    """

    _DEFAULT_API_TIMEOUT = 10

    def __init__(self, *args: Any, **kwargs: Any):
        """Construct a HumeBatchClient.

        Args:
            api_key (str): Hume API key.
        """
        super().__init__(*args, **kwargs)

    def get_job_result(self, job_id: str) -> BatchJobResult:
        """Get the result of the batch job.

        Args:
            job_id (str): Job ID.

        Raises:
            HumeClientError: If the job result cannot be loaded.

        Returns:
            BatchJobResult: Batch job result.
        """
        endpoint = (f"{self._api_http_base_url}/{self._api_version}/{ApiType.BATCH.value}/jobs/{job_id}"
                    f"?apikey={self._api_key}")
        response = requests.get(endpoint, timeout=self._DEFAULT_API_TIMEOUT)
        try:
            body = response.json()
        except json.JSONDecodeError:
            # pylint: disable=raise-missing-from
            raise HumeClientError("Unexpected error when getting job result")

        if "message" in body and body["message"] == "job not found":
            raise HumeClientError(f"Could not find a job with ID {job_id}")

        return BatchJobResult.from_response(body)

    def submit_face(
        self,
        urls: List[str],
        fps_pred: Optional[float] = None,
        prob_threshold: Optional[float] = None,
        identify_faces: Optional[bool] = None,
        min_face_size: Optional[float] = None,
    ) -> BatchJob:
        """Submit a new job for facial expression.

        Args:
            urls (List[str]): URLs to process.
            fps_pred (Optional[float]): Number of frames per second to process. Other frames will be omitted
                from the response.
            prob_threshold (Optional[float]): Face detection probability threshold. Faces detected with a
                probability less than this threshold will be omitted from the response.
            identify_faces (Optional[bool]): Whether to return identifiers for faces across frames.
                If true, unique identifiers will be assigned to face bounding boxes to differentiate different faces.
                If false, all faces will be tagged with an "unknown" ID.
            min_face_size (Optional[float]): Minimum bounding box side length in pixels to treat as a face.
                Faces detected with a bounding box side length in pixels less than this threshold will be
                omitted from the response.

        Raises:
            HumeClientError: If the job fails.

        Returns:
            BatchJob: Batch job.
        """
        config = FaceConfig(
            fps_pred=fps_pred,
            prob_threshold=prob_threshold,
            identify_faces=identify_faces,
            min_face_size=min_face_size,
        )
        return self._submit(urls, [config])

    def submit_burst(
        self,
        urls: List[str],
    ) -> BatchJob:
        """Submit a new job for vocal bursts.

        Args:
            urls (List[str]): URLs to process.

        Raises:
            HumeClientError: If the job fails.

        Returns:
            BatchJob: Batch job.
        """
        config = BurstConfig()
        return self._submit(urls, [config])

    def submit_prosody(
        self,
        urls: List[str],
        identify_speakers: Optional[bool] = None,
    ) -> BatchJob:
        """Submit a new job for vocal bursts.

        Args:
            urls (List[str]): URLs to process.
            identify_speakers (Optional[bool]): Whether to return identifiers for speakers over time. If true,
                unique identifiers will be assigned to spoken words to differentiate different speakers. If false,
                all speakers will be tagged with an "unknown" ID.

        Raises:
            HumeClientError: If the job fails.

        Returns:
            BatchJob: Batch job.
        """
        config = ProsodyConfig(identify_speakers=identify_speakers)
        return self._submit(urls, [config])

    def submit_language(
        self,
        urls: List[str],
        granularity: Optional[str] = None,
        identify_speakers: Optional[bool] = None,
    ) -> BatchJob:
        """Submit a new job for language emotion.

        Args:
            urls (List[str]): URLs to process.
            granularity (Optional[str]): The granularity at which to generate predictions.
                Values are `word`, `sentence`, or `passage`. Default value is `word`.
            identify_speakers (Optional[bool]): Whether to return identifiers for speakers over time.
                If true, unique identifiers will be assigned to spoken words to differentiate different speakers.
                If false, all speakers will be tagged with an "unknown" ID.

        Raises:
            HumeClientError: If the job fails.

        Returns:
            BatchJob: Batch job.
        """
        config = LanguageConfig(
            granularity=granularity,
            identify_speakers=identify_speakers,
        )
        return self._submit(urls, [config])

    def _submit(self, urls: List[str], configs: List[JobConfigBase]) -> BatchJob:
        request = self._get_request(configs, urls)
        return self.start_job(request)

    def get_job(self, job_id: str) -> BatchJob:
        """Rehydrate a job based on a Job ID.

        Args:
            job_id (str): ID of the job to rehydrate.

        Returns:
            BatchJob: Job associated with the given ID.
        """
        return BatchJob(self, job_id)

    def start_job(self, request_body: Any) -> BatchJob:
        """Start a batch job.

        Args:
            request_body (Any): JSON request body to be passed to the batch API.

        Raises:
            HumeClientError: If the batch job fails to start.

        Returns:
            BatchJob: A `BatchJob` that wraps the batch computation.
        """
        endpoint = (f"{self._api_http_base_url}/{self._api_version}/{ApiType.BATCH.value}/jobs"
                    f"?apikey={self._api_key}")
        response = requests.post(endpoint, json=request_body, timeout=self._DEFAULT_API_TIMEOUT)

        try:
            body = response.json()
        except json.decoder.JSONDecodeError:
            # pylint: disable=raise-missing-from
            raise HumeClientError(f"Failed batch request: {response.text}")

        if "job_id" not in body:
            if "fault" in body and "faultstring" in body["fault"]:
                fault_string = body["fault"]["faultstring"]
                raise HumeClientError(f"Could not start batch job: {fault_string}")
            raise HumeClientError("Unexpected error when starting batch job")

        return BatchJob(self, body["job_id"])

    @classmethod
    def _get_request(cls, configs: List[JobConfigBase], urls: List[str]) -> Dict[str, Any]:
        model_requests = {}
        for config in configs:
            model_requests[config.get_model_type().value] = config.serialize()

        return {
            "models": model_requests,
            "urls": urls,
        }
