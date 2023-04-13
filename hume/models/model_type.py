"""Model type enum."""
from enum import Enum


class ModelType(Enum):
    """Model type enum."""

    BURST = "burst"
    FACE = "face"
    FACEMESH = "facemesh"
    LANGUAGE = "language"
    NER = "ner"
    PROSODY = "prosody"

    @classmethod
    def from_str(cls, model_type: str) -> "ModelType":
        """Get the `ModelType` variant from a string.

        Args:
            model_type (str): Model type string.

        Raises:
            ValueError: If the model type string cannot be converted.

        Returns:
            ModelType: `ModelType` variant based on the given string.
        """
        for _, enum_value in cls.__members__.items():
            if enum_value.value == model_type:
                return enum_value
        raise ValueError(f"Unknown model type '{model_type}'")
