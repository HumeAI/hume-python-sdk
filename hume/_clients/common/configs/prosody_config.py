from typing import Any, Dict, Optional

from hume._clients.common.configs.model_config_base import ModelConfigBase
from hume._clients.common.model_type import ModelType


class ProsodyConfig(ModelConfigBase["ProsodyConfig"]):

    def __init__(
        self,
        identify_speakers: Optional[bool] = None,
    ):
        self.identify_speakers = identify_speakers

    def get_model_type(cls) -> ModelType:
        return ModelType.PROSODY

    def serialize(self) -> Dict[str, Any]:
        return {
            "identify_speakers": self.identify_speakers,
        }

    @classmethod
    def deserialize(cls, request_dict: Dict[str, Any]) -> "ProsodyConfig":
        return cls(identify_speakers=request_dict["identify_speakers"])
