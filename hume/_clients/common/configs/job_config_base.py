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
            ModelType: Model type.
        """
        pass

    @abstractmethod
    def serialize(self) -> Dict[str, Any]:
        """Serialize configuration to dictionary.

        Returns:
            Dict[str, Any]: Serialized configuration object.
        """
        pass

    @classmethod
    @abstractmethod
    def deserialize(cls, request_dict: Dict[str, Any]) -> TConfig:
        """Deserialize configuration from request JSON.

        Args:
            request_dict (Dict[str, Any]): Request JSON data.

        Returns:
            TConfig: Deserialized configuration object.
        """
        pass
