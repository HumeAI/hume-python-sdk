import pytest

from hume import ModelType


class TestModelType:

    @pytest.mark.parametrize("model_type", ["face", "prosody", "burst", "language"])
    def test_from_str(self, model_type):
        ModelType.from_str(model_type)

    def test_from_str_fail(self):
        with pytest.raises(ValueError, match="Unknown model type 'invalid'"):
            ModelType.from_str("invalid")
