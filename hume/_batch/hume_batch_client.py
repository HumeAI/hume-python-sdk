"""Batch API client."""
import json
import logging
from typing import Any, Dict, List

import requests

from hume._batch.batch_job import BatchJob
from hume._batch.batch_job_result import BatchJobResult
from hume._common.config import JobConfigBase
from hume._common.api_type import ApiType
from hume._common.client_base import ClientBase
from hume._common.hume_client_exception import HumeClientException

logger = logging.getLogger(__name__)


class HumeBatchClient(ClientBase):
    """Batch API client.

    Example:
        ```python
        from hume import HumeBatchClient
        from hume.config import FaceConfig

        client = HumeBatchClient("<your-api-key>")
        configs = [FaceConfig(identify_faces=True)]
        job = client.submit(["<your-image-url>"], configs)

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
            HumeClientException: If the job result cannot be loaded.

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
            raise HumeClientException("Unexpected error when getting job result")

        if "message" in body and body["message"] == "job not found":
            raise HumeClientException(f"Could not find a job with ID {job_id}")

        return BatchJobResult.from_response(body)

    def submit(self, urls: List[str], configs: List[JobConfigBase]) -> BatchJob:
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
            HumeClientException: If the batch job fails to start.

        Returns:
            BatchJob: A `BatchJob` that wraps the batch computation.
        """
        endpoint = f"{self._api_http_base_url}/{self._api_version}/{ApiType.BATCH.value}/jobs"

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
                fault_string = body["fault"]["faultstring"]
                raise HumeClientException(f"Could not start batch job: {fault_string}")
            raise HumeClientException("Unexpected error when starting batch job")

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
