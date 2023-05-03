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
    """

    language: Optional[str] = None
