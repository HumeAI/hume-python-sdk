"""Batch job result."""
import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from hume._batch.batch_job_state import BatchJobState
from hume._batch.batch_job_status import BatchJobStatus
from hume._common.config_utils import config_from_model_type
from hume.error.hume_client_exception import HumeClientException
from hume.models import ModelType
from hume.models.config.model_config_base import ModelConfigBase


class BatchJobResult:
    """Batch job result."""

    def __init__(
        self,
        *,
        configs: Dict[ModelType, ModelConfigBase],
        urls: List[str],
        files: List[str],
        callback_url: Optional[str],
        notify: bool,
        state: BatchJobState,
    ):
        """Construct a BatchJobResult.

        Args:
            configs (Dict[ModelType, ModelConfigBase]): Configurations for the `BatchJob`.
            urls (List[str]): URLs processed in the `BatchJob`.
            files (List[str]): Files processed in the `BatchJob`.
            callback_url (Optional[str]): A URL to which a POST request is sent upon job completion.
            notify (bool): Whether an email notification should be sent upon job completion.
            state (BatchJobState): State of `BatchJob`.
        """
        self.configs = configs
        self.urls = urls
        self.files = files
        self.callback_url = callback_url
        self.notify = notify
        self.state = state

    # def download_predictions(self, filepath: Optional[Union[str, Path]] = None) -> None:
    #     """Download `BatchJob` predictions file.

    #     Args:
    #         filepath (Optional[Union[str, Path]]): Filepath where predictions will be downloaded.
    #     """
    #     if self.predictions_url is None:
    #         raise HumeClientException("Could not download job predictions. No predictions found on job result.")
    #     urlretrieve(self.predictions_url, filepath)

    # def download_artifacts(self, filepath: Optional[Union[str, Path]] = None) -> None:
    #     """Download `BatchJob` artifacts zip archive.

    #     Args:
    #         filepath (Optional[Union[str, Path]]): Filepath where artifacts zip archive will be downloaded.
    #     """
    #     if self.artifacts_url is None:
    #         raise HumeClientException("Could not download job artifacts. No artifacts found on job result.")
    #     urlretrieve(self.artifacts_url, filepath)

    # def download_errors(self, filepath: Optional[Union[str, Path]] = None) -> None:
    #     """Download `BatchJob` errors file.

    #     Args:
    #         filepath (Optional[Union[str, Path]]): Filepath where errors will be downloaded.
    #     """
    #     if self.errors_url is None:
    #         raise HumeClientException("Could not download job errors. No errors found on job result.")
    #     urlretrieve(self.errors_url, filepath)

    @classmethod
    def from_response(cls, response: Any) -> "BatchJobResult":
        """Construct a `BatchJobResult` from a batch API job response.

        Args:
            response (Any): Batch API job response.

        Returns:
            BatchJobResult: A `BatchJobResult` based on a batch API job response.
        """
        try:
            request = response["request"]

            configs = {}
            for model_name, config_dict in request["models"].items():
                model_type = ModelType.from_str(model_name)
                config = config_from_model_type(model_type).from_dict(config_dict)
                configs[model_type] = config

            urls = request["urls"]
            files = request["files"]
            callback_url = request["callback_url"]
            notify = request["notify"]

            state_dict = response["state"]
            state = BatchJobState(
                BatchJobStatus.from_str(state_dict["status"]),
                state_dict["created_timestamp_ms"],
                state_dict["started_timestamp_ms"],
                state_dict["ended_timestamp_ms"],
            )

            return cls(
                configs=configs,
                urls=urls,
                files=files,
                callback_url=callback_url,
                notify=notify,
                state=state,
            )
        # pylint: disable=broad-except
        except Exception as exc:
            message = cls._get_invalid_response_message(response)
            raise HumeClientException(message) from exc

    @classmethod
    def _get_invalid_response_message(cls, response: Any) -> str:
        response_str = json.dumps(response)
        message = f"Could not parse response into BatchJobResult: {response_str}"

        # Check for invalid API key
        if "fault" in response and "faultstring" in response["fault"]:
            fault_string = response["fault"]["faultstring"]
            if fault_string == "Invalid ApiKey":
                message = "HumeBatchClient initialized with invalid API key."

        return message
