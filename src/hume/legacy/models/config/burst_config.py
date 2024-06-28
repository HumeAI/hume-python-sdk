"""Configuration for the vocal burst model."""

from dataclasses import dataclass

from hume.legacy.models import ModelType
from hume.legacy.models.config.model_config_base import ModelConfigBase


@dataclass
class BurstConfig(ModelConfigBase):
    """Configuration for the vocal burst model."""

    @classmethod
    def get_model_type(cls) -> ModelType:
        """Get the configuration model type.

        Returns:
            ModelType: Model type.
        """
        return ModelType.BURST
