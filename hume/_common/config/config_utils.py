"""Model configuration utilities."""
from typing import Type

from hume._common.model_type import ModelType
from hume._common.config import BurstConfig, FaceConfig, FacemeshConfig, LanguageConfig, JobConfigBase, ProsodyConfig
from hume._common.hume_client_error import HumeClientError


def config_from_model_type(model_type: ModelType) -> Type[JobConfigBase]:
    """Get the configuration type for the given model type.

    Args:
        model_type (ModelType): Model type of configuration.

    Returns:
        Type[JobConfigBase]: Class of configuration for the given model type.
    """
    if model_type == ModelType.BURST:
        return BurstConfig
    if model_type == ModelType.FACE:
        return FaceConfig
    if model_type == ModelType.FACEMESH:
        return FacemeshConfig
    if model_type == ModelType.LANGUAGE:
        return LanguageConfig
    if model_type == ModelType.PROSODY:
        return ProsodyConfig
    raise HumeClientError(f"Unknown model type {model_type}")
