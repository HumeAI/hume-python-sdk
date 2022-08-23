"""Abstract base class for model configurations."""
from abc import ABC, abstractmethod
from typing import Any, Dict, Generic, TypeVar

from hume._clients.common.model_type import ModelType

TConfig = TypeVar("TConfig")  # Type for subclasses of JobConfigBase


class JobConfigBase(ABC, Generic[TConfig]):
    """Abstract base class for model configurations."""

    @classmethod
    @abstractmethod
    def get_model_type(cls) -> ModelType:
        """Get the configuration model type.

        Returns:
            Model type.
        """
        pass

    @abstractmethod
    def serialize(self) -> Dict[str, Any]:
        """Serialize configuration to dictionary.

        Returns:
            Serialized configuration object.
        """
        pass

    @classmethod
    @abstractmethod
    def deserialize(cls, request_dict: Dict[str, Any]) -> TConfig:
        """Deserialize configuration from request JSON.

        Args:
            request_dict: Request JSON data.

        Returns:
            Deserialized configuration object.
        """
        pass
