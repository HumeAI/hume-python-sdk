"""Model configuration utilities."""
from typing import Any, Dict, List, Type

from hume.error.hume_client_exception import HumeClientException
from hume.models import ModelType
from hume.models.config import BurstConfig, FaceConfig, FacemeshConfig, LanguageConfig, ModelConfigBase, ProsodyConfig


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
    if model_type == ModelType.PROSODY:
        return ProsodyConfig
    raise HumeClientException(f"Unknown model type {model_type}")


def serialize_configs(configs: List[ModelConfigBase]) -> Dict[str, Dict[str, Any]]:
    serialized = {}
    for config in configs:
        model_type = config.get_model_type()
        model_name = model_type.value
        serialized[model_name] = config.serialize()
    return serialized


def configs_from_dict(models_config_json: Dict[str, Dict[str, Any]]) -> List[ModelConfigBase]:
    configs = []
    for model_name, config_dict in models_config_json.items():
        model_type = ModelType.from_str(model_name)
        config = config_from_model_type(model_type).deserialize(config_dict)
        configs.append(config)
    return configs
