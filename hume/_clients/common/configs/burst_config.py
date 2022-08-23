"""Configuration for the vocal burst model."""
from typing import Any, Dict

from hume._clients.common.configs.job_config_base import JobConfigBase
from hume._clients.common.model_type import ModelType


class BurstConfig(JobConfigBase["BurstConfig"]):
    """Configuration for the vocal burst model."""

    def get_model_type(cls) -> ModelType:
        """Get the configuration model type.

        Returns:
            Model type.
        """
        return ModelType.BURST

    def serialize(self) -> Dict[str, Any]:
        """Serialize BurstConfig to dictionary.

        Returns:
            Serialized BurstConfig object.
        """
        return {}

    @classmethod
    def deserialize(cls, request_dict: Dict[str, Any]) -> "BurstConfig":
        """Deserialize BurstConfig from request JSON.

        Args:
            request_dict: Request JSON data.

        Returns:
            Deserialized BurstConfig object.
        """
        return cls()
