"""Configuration for the language emotion model."""
from typing import Any, Dict, Optional

from hume._common.config.job_config_base import JobConfigBase
from hume._common.model_type import ModelType


class LanguageConfig(JobConfigBase["LanguageConfig"]):
    """Configuration for the language emotion model."""

    def __init__(
        self,
        *,
        granularity: Optional[str] = None,
        identify_speakers: Optional[bool] = None,
    ):
        """Construct a `LanguageConfig`.

        Args:
            granularity (Optional[str]): The granularity at which to generate predictions.
                Values are `word`, `sentence`, or `passage`. Default value is `word`.
            identify_speakers (Optional[bool]): Whether to return identifiers for speakers over time.
                If true, unique identifiers will be assigned to spoken words to differentiate different speakers.
                If false, all speakers will be tagged with an "unknown" ID.
        """
        self.granularity = granularity
        self.identify_speakers = identify_speakers

    @classmethod
    def get_model_type(cls) -> ModelType:
        """Get the configuration model type.

        Returns:
            ModelType: Model type.
        """
        return ModelType.LANGUAGE

    def serialize(self) -> Dict[str, Any]:
        """Serialize `LanguageConfig` to dictionary.

        Returns:
            Dict[str, Any]: Serialized `LanguageConfig` object.
        """
        return {
            "granularity": self.granularity,
            "identify_speakers": self.identify_speakers,
        }

    @classmethod
    def deserialize(cls, request_dict: Dict[str, Any]) -> "LanguageConfig":
        """Deserialize `LanguageConfig` from request JSON.

        Args:
            request_dict (Dict[str, Any]): Request JSON data.

        Returns:
            LanguageConfig: Deserialized `LanguageConfig` object.
        """
        return cls(
            granularity=request_dict.get("granularity"),
            identify_speakers=request_dict.get("identify_speakers"),
        )
