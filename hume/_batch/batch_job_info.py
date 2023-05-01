"""Batch job info."""
import json
from typing import Any, Dict, List, Optional

from hume._batch.batch_job_state import BatchJobState
from hume._batch.batch_job_status import BatchJobStatus
from hume._common.config_utils import config_from_model_type
from hume.error.hume_client_exception import HumeClientException
from hume.models import ModelType
from hume.models.config.model_config_base import ModelConfigBase


class BatchJobInfo:
    """Batch job info."""

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
        """Construct a BatchJobInfo.

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

    @classmethod
    def from_response(cls, response: Any) -> "BatchJobInfo":
        """Construct a `BatchJobInfo` from a batch API job response.

        Args:
            response (Any): Batch API job response.

        Returns:
            BatchJobInfo: A `BatchJobInfo` based on a batch API job response.
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
        message = f"Could not parse response into BatchJobInfo: {response_str}"

        # Check for invalid API key
        if "fault" in response and "faultstring" in response["fault"]:
            fault_string = response["fault"]["faultstring"]
            if fault_string == "Invalid ApiKey":
                message = "HumeBatchClient initialized with invalid API key."

        return message
