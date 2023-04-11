"""Abstract base class for model configurations."""
import warnings
from abc import abstractmethod, ABC
from dataclasses import asdict, dataclass, fields
from typing import Any, Dict, Generic, TypeVar

from hume.models import ModelType

T = TypeVar("T")  # Type for subclasses of ModelConfigBase


@dataclass
class ModelConfigBase(ABC, Generic[T]):
    """Abstract base class for model configurations."""

    @classmethod
    @abstractmethod
    def get_model_type(cls) -> ModelType:
        """Get the configuration model type.

        Returns:
            ModelType: Model type.
        """

    def serialize(self, skip_none: bool = True) -> Dict[str, Any]:
        """Serialize configuration to dictionary.

        Args:
            skip_none (bool): Whether None configurations should be skipped during serialization.

        Returns:
            Dict[str, Any]: Serialized configuration object.
        """
        return {k: v for k, v in asdict(self).items() if v is not None or not skip_none}

    @classmethod
    def deserialize(cls, request_dict: Dict[str, Any]) -> "ModelConfigBase[T]":
        """Deserialize configuration from request JSON.

        Args:
            request_dict (Dict[str, Any]): Request JSON data.

        Returns:
            T: Deserialized configuration object.
        """
        class_fields = set(field.name for field in fields(cls))
        removal_params = []
        for param in request_dict:
            if param not in class_fields:
                removal_params.append(param)
                class_name = cls.__name__
                warnings.warn(f"Got an unknown parameter `{param}` when loading `{class_name}`. "
                              "Your installed version of the Python SDK may be out of date "
                              "with the latest Hume APIs. "
                              "Run `pip install --upgrade hume` to get the latest version of the Python SDK.")
        for removal_param in removal_params:
            request_dict.pop(removal_param)

        return cls(**request_dict)
