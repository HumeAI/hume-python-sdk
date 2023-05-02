"""Configuration for speech transcription."""
from dataclasses import dataclass
from typing import Optional

from hume._common.config_base import ConfigBase


@dataclass
class TranscriptionConfig(ConfigBase["TranscriptionConfig"]):
    """Configuration for speech transcription.

    Args:
        language (Optional[str]): The BCP-47 tag (see above) of the language spoken in your media samples;
            If missing or null, it will be automatically detected. Values are `zh`, `da`, `nl`, `en`, `en-AU`,
            `en-IN`, `en-NZ`, `en-GB`, `fr`, `fr-CA`, `de`, `hi`, `hi-Latn`, `id`, `it`, `ja`, `ko`, `no`,
            `pl`, `pt`, `pt-BR`, `pt-PT`, `ru`, `es`, `es-419`, `sv`, `ta`, `tr`, or `uk`.
            This configuration is not available for the streaming API.
        identify_speakers (Optional[bool]): Whether to return identifiers for speakers over time.
            If true, unique identifiers will be assigned to spoken words to differentiate different speakers.
            If false, all speakers will be tagged with an "unknown" ID.
            This configuration is not available for the streaming API.
    """

    language: Optional[str] = None
    identify_speakers: Optional[bool] = None
