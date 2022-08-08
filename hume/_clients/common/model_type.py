from enum import Enum


class ModelType(Enum):
    BURST = 'burst'
    FACE = 'face'
    LANGUAGE = 'language'
    PROSODY = 'prosody'

    @classmethod
    def from_str(cls, model_type: str) -> 'ModelType':
        for _, enum_value in cls.__members__.items():
            if enum_value.value == model_type:
                return enum_value
        raise ValueError(f"Unknown model type '{model_type}'")
