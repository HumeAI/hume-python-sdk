"""Configuration for the vocal burst model."""
from typing import Any, Dict

from hume.models import ModelType
from hume.models.config.model_config_base import ModelConfigBase


class BurstConfig(ModelConfigBase["BurstConfig"]):
    """Configuration for the vocal burst model."""

    @classmethod
    def get_model_type(cls) -> ModelType:
        """Get the configuration model type.

        Returns:
            ModelType: Model type.
        """
        return ModelType.BURST

    def serialize(self) -> Dict[str, Any]:
        """Serialize `BurstConfig` to dictionary.

        Returns:
            Dict[str, Any]: Serialized `BurstConfig` object.
        """
        return {}

    @classmethod
    def deserialize(cls, request_dict: Dict[str, Any]) -> "BurstConfig":
        """Deserialize `BurstConfig` from request JSON.

        Args:
            request_dict (Dict[str, Any]): Request JSON data.

        Returns:
            BurstConfig: Deserialized `BurstConfig` object.
        """
        return cls()
