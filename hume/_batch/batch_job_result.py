"""Batch job result."""
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from urllib.request import urlretrieve

from hume._batch.batch_job_status import BatchJobStatus
from hume._common.model_type import ModelType
from hume._common.config.job_config_base import JobConfigBase
from hume._common.config.config_utils import config_from_model_type
from hume._common.hume_client_error import HumeClientError


class BatchJobResult:
    """Batch job result."""

    def __init__(
        self,
        *,
        configs: Dict[ModelType, JobConfigBase],
        urls: List[str],
        status: BatchJobStatus,
        predictions_url: Optional[str] = None,
        artifacts_url: Optional[str] = None,
        errors_url: Optional[str] = None,
        error_message: Optional[str] = None,
        job_start_time: Optional[int] = None,
        job_end_time: Optional[int] = None,
    ):
        """Construct a BatchJobResult.

        Args:
            configs (Dict[ModelType, JobConfigBase]): Configurations for the `BatchJob`.
            urls (List[str]): URLs processed in the `BatchJob`.
            status (BatchJobStatus): Status of `BatchJob`.
            predictions_url (Optional[str]): URL to predictions file.
            artifacts_url (Optional[str]): URL to artifacts zip archive.
            errors_url (Optional[str]): URL to errors file.
            error_message (Optional[str]): Error message for request.
            job_start_time (Optional[int]): Time when job started.
            job_end_time (Optional[int]): Time when job completed.
        """
        self.configs = configs
        self.urls = urls
        self.status = status
        self.predictions_url = predictions_url
        self.artifacts_url = artifacts_url
        self.errors_url = errors_url
        self.error_message = error_message
        self.job_start_time = job_start_time
        self.job_end_time = job_end_time

    def download_predictions(self, filepath: Optional[Union[str, Path]] = None) -> None:
        """Download `BatchJob` predictions file.

        Args:
            filepath (Optional[Union[str, Path]]): Filepath where predictions will be downloaded.
        """
        if self.predictions_url is None:
            raise HumeClientError("Could not download job predictions. No predictions found on job result.")
        urlretrieve(self.predictions_url, filepath)

    def download_artifacts(self, filepath: Optional[Union[str, Path]] = None) -> None:
        """Download `BatchJob` artifacts zip archive.

        Args:
            filepath (Optional[Union[str, Path]]): Filepath where artifacts zip archive will be downloaded.
        """
        if self.artifacts_url is None:
            raise HumeClientError("Could not download job artifacts. No artifacts found on job result.")
        urlretrieve(self.artifacts_url, filepath)

    def download_errors(self, filepath: Optional[Union[str, Path]] = None) -> None:
        """Download `BatchJob` errors file.

        Args:
            filepath (Optional[Union[str, Path]]): Filepath where errors will be downloaded.
        """
        if self.errors_url is None:
            raise HumeClientError("Could not download job errors. No errors found on job result.")
        urlretrieve(self.errors_url, filepath)

    def get_error_message(self) -> Optional[str]:
        """Get any available error messages on the job.

        Returns:
            Optional[str]: A string with the error message if there was an error, otherwise `None`.
        """
        return self.error_message

    def get_run_time(self) -> Optional[int]:
        """Get the total time in seconds it took for the job to run if the job is in a terminal state.

        Returns:
            Optional[int]: Time in seconds it took for the job to run. If the job is not in a terminal
                state then `None` is returned.
        """
        if self.job_start_time is not None and self.job_end_time is not None:
            return self.job_end_time - self.job_start_time
        return None

    def get_start_time(self) -> Optional[datetime]:
        """Get the time the job started running.

        Returns:
            Optional[datetime]: Datetime when the job started running. If the job has not started
                then `None` is returned.
        """
        if self.job_start_time is None:
            return None
        return datetime.utcfromtimestamp(self.job_start_time)

    def get_end_time(self) -> Optional[datetime]:
        """Get the time the job stopped running if the job is in a terminal state.

        Returns:
            Optional[datetime]: Datetime when the job started running. If the job is not in a terminal
                state then `None` is returned.
        """
        if self.job_end_time is None:
            return None
        return datetime.utcfromtimestamp(self.job_end_time)

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
                config = config_from_model_type(model_type).deserialize(config_dict)
                configs[model_type] = config

            kwargs = {}
            if "completed" in response:
                completed_dict = response["completed"]
                kwargs["artifacts_url"] = completed_dict["artifacts_url"]
                kwargs["errors_url"] = completed_dict["errors_url"]
                kwargs["predictions_url"] = completed_dict["predictions_url"]

            if "failed" in response:
                failed_dict = response["failed"]
                if "message" in failed_dict:
                    kwargs["error_message"] = failed_dict["message"]

            if "creation_timestamp" in response:
                kwargs["job_start_time"] = response["creation_timestamp"]

            if "completion_timestamp" in response:
                kwargs["job_end_time"] = response["completion_timestamp"]

            return cls(
                configs=configs,
                urls=request["urls"],
                status=BatchJobStatus.from_str(response["status"]),
                **kwargs,
            )
        # pylint: disable=broad-except
        except Exception as exc:
            message = cls._get_invalid_response_message(response)
            raise HumeClientError(message) from exc

    @classmethod
    def _get_invalid_response_message(cls, response: Any) -> str:
        response_str = json.dumps(response)
        message = f"Could not parse response into BatchJobResult: {response_str}"

        # Check for invalid API key
        if "fault" in response and "faultstring" in response["fault"]:
            fault_string = response["fault"]["faultstring"]
            if fault_string == "Invalid ApiKey":
                message = "Client initialized with invalid API key"

        return message
