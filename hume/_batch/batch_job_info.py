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
        state: BatchJobState,
        callback_url: Optional[str] = None,
        notify: bool = False,
    ):
        """Construct a BatchJobInfo.

        Args:
            configs (Dict[ModelType, ModelConfigBase]): Configurations for the `BatchJob`.
            urls (List[str]): URLs processed in the `BatchJob`.
            files (List[str]): Files processed in the `BatchJob`.
            state (BatchJobState): State of `BatchJob`.
            callback_url (Optional[str]): A URL to which a POST request is sent upon job completion.
            notify (bool): Whether an email notification should be sent upon job completion.
        """
        self.configs = configs
        self.urls = urls
        self.files = files
        self.state = state
        self.callback_url = callback_url
        self.notify = notify

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
                if config_dict is None:
                    continue
                model_type = ModelType.from_str(model_name)
                config = config_from_model_type(model_type).from_dict(config_dict)
                configs[model_type] = config

            urls = request["urls"]
            files = request["files"]
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
        message = f"Could not parse response into BatchJobInfo: {response_str}"

        # Check for invalid API key
        if "fault" in response and "faultstring" in response["fault"]:
            fault_string = response["fault"]["faultstring"]
            if fault_string == "Invalid ApiKey":
                message = "HumeBatchClient initialized with invalid API key."

        return message
