import re

import pytest

from hume.models import ModelType


class TestModelType:

    @pytest.mark.parametrize("model_name", ["burst", "face", "facemesh", "language", "prosody"])
    def test_from_str(self, model_name: str) -> None:
        ModelType.from_str(model_name)

    def test_from_str_fail(self) -> None:
        message = "Unknown model type 'invalid'"
        with pytest.raises(ValueError, match=re.escape(message)):
            ModelType.from_str("invalid")
