"""Abstract base class for model configurations."""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic, TypeVar

from hume._common.config_base import ConfigBase
from hume.models import ModelType

T = TypeVar("T")  # Type for subclasses of ModelConfigBase


@dataclass
class ModelConfigBase(ConfigBase["ModelConfigBase"], ABC, Generic[T]):
    """Abstract base class for model configurations."""

    @classmethod
    @abstractmethod
    def get_model_type(cls) -> ModelType:
        """Get the configuration model type.

        Returns:
            ModelType: Model type.
        """
