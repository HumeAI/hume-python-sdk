"""Configuration for the named-entity emotion model."""
from dataclasses import dataclass

from hume.models import ModelType
from hume.models.config.model_config_base import ModelConfigBase


@dataclass
class NerConfig(ModelConfigBase["NerConfig"]):
    """Configuration for the named-entity emotion model.

    This model is not available for the streaming API.
    """

    @classmethod
    def get_model_type(cls) -> ModelType:
        """Get the configuration model type.

        Returns:
            ModelType: Model type.
        """
        return ModelType.NER
