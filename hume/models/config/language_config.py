"""Configuration for the language emotion model."""
from dataclasses import dataclass
from typing import Any, Dict, Optional

from hume.models import ModelType
from hume.models.config.model_config_base import ModelConfigBase


@dataclass
class LanguageConfig(ModelConfigBase["LanguageConfig"]):
    """Configuration for the language emotion model.

    Args:
        language (Optional[str]): The BCP-47 tag (see above) of the language spoken in your media samples;
            If missing or null, it will be automatically detected. Values are `zh`, `da`, `nl`, `en`, `en-AU`,
            `en-IN`, `en-NZ`, `en-GB`, `fr`, `fr-CA`, `de`, `hi`, `hi-Latn`, `id`, `it`, `ja`, `ko`, `no`,
            `pl`, `pt`, `pt-BR`, `pt-PT`, `ru`, `es`, `es-419`, `sv`, `ta`, `tr`, or `uk`.
            This configuration is not available for the streaming API.
        granularity (Optional[str]): The granularity at which to generate predictions.
            Values are `word`, `sentence`, or `passage`. Default value is `word`.
            This configuration is not available for the streaming API.
        identify_speakers (Optional[bool]): Whether to return identifiers for speakers over time.
            If true, unique identifiers will be assigned to spoken words to differentiate different speakers.
            If false, all speakers will be tagged with an "unknown" ID.
            This configuration is not available for the streaming API.
        use_existing_partition: Whether to generate predictions for speech utterances
            (rather than the user specified granularity) for text created from audio transcripts.
            This configuration is not available for the streaming API.
        sentiment (Optional[Dict[str, Any]]): Sentiment prediction can be enabled by setting "sentiment": {}.
            Currently, sentiment prediction cannot be further configured with any parameters.
            If missing or null, no sentiment predictions will be generated.
        toxicity (Optional[Dict[str, Any]]): Toxicity prediction can be enabled by setting "toxicity": {}.
            Currently, toxicity prediction cannot be further configured with any parameters.
            If missing or null, no toxicity predictions will be generated.
    """

    language: Optional[str] = None
    granularity: Optional[str] = None
    identify_speakers: Optional[bool] = None
    use_existing_partition: Optional[bool] = None
    sentiment: Optional[Dict[str, Any]] = None
    toxicity: Optional[Dict[str, Any]] = None

    @classmethod
    def get_model_type(cls) -> ModelType:
        """Get the configuration model type.

        Returns:
            ModelType: Model type.
        """
        return ModelType.LANGUAGE
