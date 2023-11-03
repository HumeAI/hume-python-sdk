"""Configuration for speech transcription."""
from dataclasses import dataclass
from typing import Optional

from hume._common.config_base import ConfigBase


@dataclass
class TranscriptionConfig(ConfigBase["TranscriptionConfig"]):
    """Configuration for speech transcription.

    Args:
        language (Optional[str]): By default, we use an automated language detection method for our
            Speech Prosody, Language, and NER models. However, if you know what language is being spoken
            in your media samples, you can specify it via its BCP-47 tag and potentially obtain more accurate results.
            You can specify any of the following: `zh`, `da`, `nl`, `en`, `en-AU`,
            `en-IN`, `en-NZ`, `en-GB`, `fr`, `fr-CA`, `de`, `hi`, `hi-Latn`, `id`, `it`, `ja`, `ko`, `no`,
            `pl`, `pt`, `pt-BR`, `pt-PT`, `ru`, `es`, `es-419`, `sv`, `ta`, `tr`, or `uk`.
        identify_speakers (Optional[bool]): Whether to return identifiers for speakers over time. If true,
            unique identifiers will be assigned to spoken words to differentiate different speakers. If false,
            all speakers will be tagged with an "unknown" ID.
            This configuration is only available for the batch API.
        prob_threshold (Optional[float]): Transcript confidence threshold. Transcripts generated with a confidence
            less than this threshold will be considered invalid and not used as an input for model inference.
    """

    language: Optional[str] = None
    identify_speakers: Optional[bool] = None
    prob_threshold: Optional[float] = None
