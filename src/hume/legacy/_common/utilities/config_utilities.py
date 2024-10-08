"""Model configuration utilities."""

from collections.abc import Iterable
from typing import Any, Type

from hume.legacy.error.hume_client_exception import HumeClientException
from hume.legacy.models import ModelType
from hume.legacy.models.config import (
    BurstConfig,
    FaceConfig,
    FacemeshConfig,
    LanguageConfig,
    ModelConfigBase,
    NerConfig,
    ProsodyConfig,
)


def config_from_model_type(model_type: ModelType) -> Type[ModelConfigBase]:
    """Get the configuration type for the given model type.

    Args:
        model_type (ModelType): Model type of configuration.

    Returns:
        Type[ModelConfigBase]: Class of configuration for the given model type.
    """
    if model_type == ModelType.BURST:
        return BurstConfig
    if model_type == ModelType.FACE:
        return FaceConfig
    if model_type == ModelType.FACEMESH:
        return FacemeshConfig
    if model_type == ModelType.LANGUAGE:
        return LanguageConfig
    if model_type == ModelType.NER:
        return NerConfig
    if model_type == ModelType.PROSODY:
        return ProsodyConfig
    raise HumeClientException(f"Unknown model type {model_type}")


def serialize_configs(configs: Iterable[ModelConfigBase]) -> dict[str, dict[str, Any]]:
    """Convert a list of configs into a dict from model name to serialized model config.

    Args:
        configs (Iterable[ModelConfigBase]): List of configuration objects.

    Returns:
        dict[str, dict[str, Any]]: Dictionary of serialized model configurations.
    """
    configs_dict = {}
    for config in configs:
        model_type = config.get_model_type()
        model_name = model_type.value
        configs_dict[model_name] = config.to_dict()
    return configs_dict


def deserialize_configs(configs_dict: dict[str, dict[str, Any]]) -> list[ModelConfigBase]:
    """Convert a dict of serialized model configs into a list of config objects.

    Args:
        configs_dict (dict[str, dict[str, Any]]): Dictionary of serialized model configurations.

    Returns:
        list[ModelConfigBase]: list of deserialized configuration objects.
    """
    configs = []
    for model_name, config_dict in configs_dict.items():
        model_type = ModelType.from_str(model_name)
        config = config_from_model_type(model_type).from_dict(config_dict)
        configs.append(config)
    return configs
