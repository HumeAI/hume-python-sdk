import pytest

from hume.legacy._common.utilities.config_utilities import config_from_model_type
from hume.legacy.models import ModelType


class TestModelConfigs:

    @pytest.mark.parametrize("model_name", ["burst", "face", "facemesh", "language", "prosody"])
    def test_get_model_type(self, model_name: str) -> None:
        model_type = ModelType.from_str(model_name)
        config = config_from_model_type(model_type)()
        assert config.get_model_type() == model_type

    @pytest.mark.parametrize("model_name", ["burst", "face", "facemesh", "language", "prosody"])
    def test_empty_serialize(self, model_name: str) -> None:
        model_type = ModelType.from_str(model_name)
        config = config_from_model_type(model_type)()
        assert config.to_dict() == {}

    @pytest.mark.parametrize("model_name", ["burst", "face", "facemesh", "language", "prosody"])
    def test_empty_deserialize(self, model_name: str) -> None:
        model_type = ModelType.from_str(model_name)
        config_class = config_from_model_type(model_type)
        config_class.from_dict({})
