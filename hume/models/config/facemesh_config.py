"""Configuration for the facial expression model."""
from dataclasses import dataclass

from hume.models import ModelType
from hume.models.config.model_config_base import ModelConfigBase


@dataclass
class FacemeshConfig(ModelConfigBase["FacemeshConfig"]):
    """Configuration for the facemesh model."""

    @classmethod
    def get_model_type(cls) -> ModelType:
        """Get the configuration model type.

        Returns:
            ModelType: Model type.
        """
        return ModelType.FACEMESH
