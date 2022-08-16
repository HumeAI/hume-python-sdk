import json
import logging
from typing import Any, Dict, List, Optional

import requests

from hume._clients.batch.batch_job import BatchJob
from hume._clients.batch.batch_job_result import BatchJobResult
from hume._clients.common.configs import BurstConfig, FaceConfig, LanguageConfig, ProsodyConfig, ModelConfigBase
from hume._clients.common.api_type import ApiType
from hume._clients.common.client_base import ClientBase
from hume._clients.common.hume_client_error import HumeClientError

logger = logging.getLogger(__name__)


class HumeBatchClient(ClientBase):

    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)

    def _start_job(self, request_body: Any) -> BatchJob:
        endpoint = (f"{self._api_base_url}/{self._api_version}/{ApiType.BATCH.value}/jobs"
                    f"?apikey={self._api_key}")
        response = requests.post(endpoint, json=request_body)

        try:
            body = response.json()
        except json.decoder.JSONDecodeError:
            raise HumeClientError(f"Failed batch request: {response.text}")

        if "job_id" not in body:
            if "fault" in body and "faultstring" in body["fault"]:
                fault_string = body["fault"]["faultstring"]
                raise HumeClientError(f"Could not start batch job: {fault_string}")
            raise HumeClientError("Unexpected error when starting batch job")

        return BatchJob(self, body["job_id"])

    def get_job_result(self, job_id: str) -> BatchJobResult:
        endpoint = (f"{self._api_base_url}/{self._api_version}/{ApiType.BATCH.value}/jobs/{job_id}"
                    f"?apikey={self._api_key}")
        response = requests.get(endpoint)
        body = response.json()
        return BatchJobResult.from_response(body)

    def _submit(self, urls: List[str], configs: List[ModelConfigBase]) -> BatchJob:
        request = self._get_request(configs, urls)
        return self._start_job(request)

    def submit_face(
        self,
        urls: List[str],
        fps_pred: Optional[float] = None,
        prob_threshold: Optional[float] = None,
        identify_faces: Optional[bool] = None,
        min_face_size: Optional[float] = None,
    ) -> BatchJob:
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
        config = BurstConfig()
        return self._submit(urls, [config])

    def submit_prosody(
        self,
        urls: List[str],
        identify_speakers: Optional[bool] = None,
    ) -> BatchJob:
        config = ProsodyConfig(identify_speakers=identify_speakers)
        return self._submit(urls, [config])

    def submit_language(
        self,
        urls: List[str],
        sliding_window: Optional[bool] = None,
    ) -> BatchJob:
        config = LanguageConfig(sliding_window=sliding_window)
        return self._submit(urls, [config])

    @classmethod
    def _get_request(cls, configs: List[ModelConfigBase], urls: List[str]) -> Dict[str, Any]:
        model_requests = {}
        for config in configs:
            model_requests[config.get_model_type().value] = config.serialize()

        return {
            "models": model_requests,
            "urls": urls,
        }
