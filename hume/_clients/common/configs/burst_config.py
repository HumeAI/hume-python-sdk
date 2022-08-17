from typing import Any, Dict

from hume._clients.common.configs.job_config_base import JobConfigBase
from hume._clients.common.model_type import ModelType


class BurstConfig(JobConfigBase["BurstConfig"]):

    def get_model_type(cls) -> ModelType:
        return ModelType.BURST

    def serialize(self) -> Dict[str, Any]:
        return {}

    @classmethod
    def deserialize(cls, request_dict: Dict[str, Any]) -> "BurstConfig":
        return cls()
