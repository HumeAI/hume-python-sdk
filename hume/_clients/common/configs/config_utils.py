from hume._clients.common.model_type import ModelType
from hume._clients.common.configs.burst_config import BurstConfig
from hume._clients.common.configs.face_config import FaceConfig
from hume._clients.common.configs.language_config import LanguageConfig
from hume._clients.common.configs.prosody_config import ProsodyConfig
from hume._clients.common.hume_client_error import HumeClientError


def config_from_model_type(model_type: ModelType):
    if model_type == ModelType.BURST:
        return BurstConfig
    elif model_type == ModelType.FACE:
        return FaceConfig
    elif model_type == ModelType.LANGUAGE:
        return LanguageConfig
    elif model_type == ModelType.PROSODY:
        return ProsodyConfig
    raise HumeClientError(f"Unknown model type {model_type}")
