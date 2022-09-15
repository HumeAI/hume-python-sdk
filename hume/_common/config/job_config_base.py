"""Abstract base class for model configurations."""
from abc import ABC, abstractmethod
from typing import Any, Dict, Generic, TypeVar

from hume._common.model_type import ModelType

T = TypeVar("T")  # Type for subclasses of JobConfigBase


class JobConfigBase(ABC, Generic[T]):
    """Abstract base class for model configurations."""

    @classmethod
    @abstractmethod
    def get_model_type(cls) -> ModelType:
        """Get the configuration model type.

        Returns:
            ModelType: Model type.
        """

    @abstractmethod
    def serialize(self) -> Dict[str, Any]:
        """Serialize configuration to dictionary.

        Returns:
            Dict[str, Any]: Serialized configuration object.
        """

    @classmethod
    @abstractmethod
    def deserialize(cls, request_dict: Dict[str, Any]) -> T:
        """Deserialize configuration from request JSON.

        Args:
            request_dict (Dict[str, Any]): Request JSON data.

        Returns:
            T: Deserialized configuration object.
        """
