"""Configuration for the named-entity emotion model."""
from dataclasses import dataclass
from typing import Optional

from hume.models import ModelType
from hume.models.config.model_config_base import ModelConfigBase


@dataclass
class NerConfig(ModelConfigBase["NerConfig"]):
    """Configuration for the named-entity emotion model.

    This model is only available for the batch API.

    Args:
        identify_speakers (Optional[bool]): Whether to return identifiers for speakers over time. If true,
            unique identifiers will be assigned to spoken words to differentiate different speakers. If false,
            all speakers will be tagged with an "unknown" ID.
            This configuration is only available for the batch API.
    """

    identify_speakers: Optional[bool] = None

    @classmethod
    def get_model_type(cls) -> ModelType:
        """Get the configuration model type.

        Returns:
            ModelType: Model type.
        """
        return ModelType.NER
