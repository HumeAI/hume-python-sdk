"""Batch job details."""
import json
from datetime import datetime
from typing import Any, Dict, List, Optional

from hume._batch.batch_job_state import BatchJobState
from hume._batch.batch_job_status import BatchJobStatus
from hume._common.config_utils import config_from_model_type
from hume.error.hume_client_exception import HumeClientException
from hume.models import ModelType
from hume.models.config.model_config_base import ModelConfigBase


class BatchJobDetails:
    """Batch job details."""

    def __init__(
        self,
        *,
        configs: Dict[ModelType, ModelConfigBase],
        urls: List[str],
        files: List[str],
        text: Optional[List[str]] = None,
        state: BatchJobState,
        callback_url: Optional[str] = None,
        notify: bool = False,
    ):
        """Construct a BatchJobDetails.

        Args:
            configs (Dict[ModelType, ModelConfigBase]): Configurations for the `BatchJob`.
            urls (List[str]): URLs processed in the `BatchJob`.
            files (List[str]): Files processed in the `BatchJob`.
            text (Optional[List[str]]): Raw text processed in the `BatchJob`.
            state (BatchJobState): State of `BatchJob`.
            callback_url (Optional[str]): A URL to which a POST request is sent upon job completion.
            notify (bool): Whether an email notification should be sent upon job completion.
        """
        self.configs = configs
        self.urls = urls
        self.files = files
        self.text = text
        self.state = state
        self.callback_url = callback_url
        self.notify = notify

    @classmethod
    def from_response(cls, response: Any) -> "BatchJobDetails":
        """Construct a `BatchJobDetails` from a batch API job response.

        Args:
            response (Any): Batch API job response.

        Returns:
            BatchJobDetails: A `BatchJobDetails` based on a batch API job response.
        """
        try:
            request = response["request"]

            configs = {}
            for model_name, config_dict in request["models"].items():
                if config_dict is None:
                    continue
                model_type = ModelType.from_str(model_name)
                config = config_from_model_type(model_type).from_dict(config_dict)
                configs[model_type] = config

            urls = request["urls"]
            files = request["files"]
            text = request["text"]
            callback_url = request["callback_url"]
            notify = request["notify"]

            state_dict = response["state"]
            state = BatchJobState(
                status=BatchJobStatus.from_str(state_dict["status"]),
                created_timestamp_ms=state_dict.get("created_timestamp_ms"),
                started_timestamp_ms=state_dict.get("started_timestamp_ms"),
                ended_timestamp_ms=state_dict.get("ended_timestamp_ms"),
            )

            return cls(
                configs=configs,
                urls=urls,
                files=files,
                text=text,
                state=state,
                callback_url=callback_url,
                notify=notify,
            )
        # pylint: disable=broad-except
        except Exception as exc:
            message = cls._get_invalid_response_message(response)
            raise HumeClientException(message) from exc

    @classmethod
    def _get_invalid_response_message(cls, response: Any) -> str:
        response_str = json.dumps(response)
        message = f"Could not parse response into BatchJobDetails: {response_str}"

        # Check for invalid API key
        if "fault" in response and "faultstring" in response["fault"]:
            fault_string = response["fault"]["faultstring"]
            if fault_string == "Invalid ApiKey":
                message = "HumeBatchClient initialized with invalid API key."

        return message

    def get_status(self) -> BatchJobStatus:
        """Get the status of the job.

        Returns:
            BatchJobStatus: The status of the `BatchJob`.
        """
        return self.state.status

    def get_run_time_ms(self) -> Optional[int]:
        """Get the total time in milliseconds it took for the job to run if the job is in a terminal state.

        Returns:
            Optional[int]: Time in milliseconds it took for the job to run. If the job is not in a terminal
                state then `None` is returned.
        """
        if self.state.started_timestamp_ms is not None and self.state.ended_timestamp_ms is not None:
            return self.state.ended_timestamp_ms - self.state.started_timestamp_ms
        return None

    def get_created_time(self) -> Optional[datetime]:
        """Get the time the job was created.

        Returns:
            Optional[datetime]: Datetime when the job was created. If the job has not started
                then `None` is returned.
        """
        if self.state.created_timestamp_ms is None:
            return None
        return datetime.utcfromtimestamp(self.state.created_timestamp_ms / 1000)

    def get_started_time(self) -> Optional[datetime]:
        """Get the time the job started running.

        Returns:
            Optional[datetime]: Datetime when the job started running. If the job has not started
                then `None` is returned.
        """
        if self.state.started_timestamp_ms is None:
            return None
        return datetime.utcfromtimestamp(self.state.started_timestamp_ms / 1000)

    def get_ended_time(self) -> Optional[datetime]:
        """Get the time the job stopped running if the job is in a terminal state.

        Returns:
            Optional[datetime]: Datetime when the job started running. If the job is not in a terminal
                state then `None` is returned.
        """
        if self.state.ended_timestamp_ms is None:
            return None
        return datetime.utcfromtimestamp(self.state.ended_timestamp_ms / 1000)
