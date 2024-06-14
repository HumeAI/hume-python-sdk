"""Abstract base class for model configurations."""

from abc import ABC, abstractmethod
from dataclasses import dataclass

from hume._common.config_base import ConfigBase
from hume.models import ModelType


@dataclass
class ModelConfigBase(ConfigBase["ModelConfigBase"], ABC):
    """Abstract base class for model configurations."""

    @classmethod
    @abstractmethod
    def get_model_type(cls) -> ModelType:
        """Get the configuration model type.

        Returns:
            ModelType: Model type.
        """
