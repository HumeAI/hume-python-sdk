"""Configuration for the speech prosody model."""
from typing import Any, Dict, Optional

from hume._clients.common.configs.job_config_base import JobConfigBase
from hume._clients.common.model_type import ModelType


class ProsodyConfig(JobConfigBase["ProsodyConfig"]):
    """Configuration for the speech prosody model."""

    def __init__(
        self,
        identify_speakers: Optional[bool] = None,
    ):
        """Construct a ProsodyConfig.

        Args:
            identify_speakers: Whether to return identifiers for speakers over time. If true, unique identifiers will
                be assigned to spoken words to differentiate different speakers. If false, all speakers will be
                tagged with an "unknown" ID.
        """
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
