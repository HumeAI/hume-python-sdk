from abc import ABC, abstractmethod
from typing import Any, Dict, Generic, TypeVar

from hume._clients.common.model_type import ModelType

TConfig = TypeVar("TConfig")  # Type for subclasses of ModelConfigBase


class ModelConfigBase(ABC, Generic[TConfig]):

    @classmethod
    @abstractmethod
    def get_model_type(cls) -> ModelType:
        pass

    @abstractmethod
    def serialize(self) -> Dict[str, Any]:
        pass

    @classmethod
    @abstractmethod
    def deserialize(cls, request_dict: Dict[str, Any]) -> TConfig:
        pass
