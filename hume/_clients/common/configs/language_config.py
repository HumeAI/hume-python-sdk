from typing import Any, Dict, Optional

from hume._clients.common.configs.model_config_base import ModelConfigBase
from hume._clients.common.model_type import ModelType


class LanguageConfig(ModelConfigBase["LanguageConfig"]):

    def __init__(
        self,
        *,
        sliding_window: Optional[float] = None,
    ):
        self.sliding_window = sliding_window

    def get_model_type(cls) -> ModelType:
        return ModelType.LANGUAGE

    def serialize(self) -> Dict[str, Any]:
        return {
            "sliding_window": self.sliding_window,
        }

    @classmethod
    def deserialize(cls, request_dict: Dict[str, Any]) -> "LanguageConfig":
        return cls(sliding_window=request_dict["sliding_window"])
