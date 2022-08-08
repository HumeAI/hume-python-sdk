import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from urllib.request import urlretrieve

from hume._clients.batch.batch_job_status import BatchJobStatus
from hume._clients.common.model_type import ModelType
from hume._clients.common.configs.model_config_base import ModelConfigBase
from hume._clients.common.configs.config_utils import config_from_model_type
from hume._clients.common.hume_client_error import HumeClientError


class BatchJobResult:

    def __init__(
        self,
        *,
        configs: Dict[ModelType, ModelConfigBase],
        urls: List[str],
        status: BatchJobStatus,
        predictions_url: Optional[str] = None,
        artifacts_url: Optional[str] = None,
        errors_url: Optional[str] = None,
    ):
        self.configs = configs
        self.urls = urls
        self.status = status
        self.artifacts_url = artifacts_url
        self.errors_url = errors_url
        self.predictions_url = predictions_url

    def download_artifacts(self, filepath: Optional[Union[str, Path]] = None) -> None:
        if self.artifacts_url is None:
            raise HumeClientError("Could not download job artifacts. No artifacts found on job result.")
        urlretrieve(self.artifacts_url, filepath)

    def download_predictions(self, filepath: Optional[Union[str, Path]] = None) -> None:
        if self.predictions_url is None:
            raise HumeClientError("Could not download job predictions. No predictions found on job result.")
        urlretrieve(self.predictions_url, filepath)

    def download_errors(self, filepath: Optional[Union[str, Path]] = None) -> None:
        if self.errors_url is None:
            raise HumeClientError("Could not download job errors. No errors found on job result.")
        urlretrieve(self.errors_url, filepath)

    @classmethod
    def from_response(cls, response: Dict[str, Any]) -> 'BatchJobResult':
        try:
            request = response["request"]
            configs = {}
            for model_name, config_dict in request["models"].items():
                model_type = ModelType.from_str(model_name)
                config = config_from_model_type(model_type).deserialize(config_dict)
                configs[model_type] = config

            kwargs = {}
            if "completed" in response:
                completed_dict = response["completed"]
                kwargs["artifacts_url"] = completed_dict["artifacts_url"]
                kwargs["errors_url"] = completed_dict["errors_url"]
                kwargs["predictions_url"] = completed_dict["predictions_url"]

            return cls(
                configs=configs,
                urls=request["urls"],
                status=BatchJobStatus.from_str(response["status"]),
                **kwargs,
            )
        except KeyError as e:
            response_str = json.dumps(response)
            raise ValueError(f"Could not parse response into BatchJobResult: {response_str}") from e
