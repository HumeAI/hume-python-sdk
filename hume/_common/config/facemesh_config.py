"""Configuration for the facial expression model."""
from typing import Any, Dict

from hume._common.config.job_config_base import JobConfigBase
from hume._common.model_type import ModelType


class FacemeshConfig(JobConfigBase["FacemeshConfig"]):
    """Configuration for the facemesh model."""

    @classmethod
    def get_model_type(cls) -> ModelType:
        """Get the configuration model type.

        Returns:
            ModelType: Model type.
        """
        return ModelType.FACEMESH

    def serialize(self) -> Dict[str, Any]:
        """Serialize `FacemeshConfig` to dictionary.

        Returns:
            Dict[str, Any]: Serialized `FacemeshConfig` object.
        """
        return {}

    @classmethod
    def deserialize(cls, request_dict: Dict[str, Any]) -> "FacemeshConfig":
        """Deserialize `FacemeshConfig` from request JSON.

        Args:
            request_dict (Dict[str, Any]): Request JSON data.

        Returns:
            FacemeshConfig: Deserialized `FacemeshConfig` object.
        """
        return cls()
