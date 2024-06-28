"""Configuration for the speech prosody model."""

from __future__ import annotations

from dataclasses import dataclass

from hume.legacy.models import ModelType
from hume.legacy.models.config.model_config_base import ModelConfigBase


@dataclass
class ProsodyConfig(ModelConfigBase):
    """Configuration for the speech prosody model.

    Args:
        granularity (str | None): The granularity at which to generate predictions.
            Accepted values are `word`, `sentence`, `utterance`, or `conversational_turn`.
            The default is `utterance`.
            `utterance` corresponds to a natural pause or break in conversation
            `conversational_turn` corresponds to a change in speaker.
            This configuration is only available for the batch API.
        identify_speakers (bool | None): Whether to return identifiers for speakers over time. If true,
            unique identifiers will be assigned to spoken words to differentiate different speakers. If false,
            all speakers will be tagged with an "unknown" ID.
            This configuration is only available for the batch API.
        window (dict[str, float] | None): Sliding window used to chunk audio.
            This dictionary input takes two entries: `length` and `step` representing
            the width of the window in seconds and the step size in seconds.
            This configuration is only available for the batch API.
    """

    identify_speakers: bool | None = None
    granularity: str | None = None
    window: dict[str, float] | None = None

    @classmethod
    def get_model_type(cls) -> ModelType:
        """Get the configuration model type.

        Returns:
            ModelType: Model type.
        """
        return ModelType.PROSODY
