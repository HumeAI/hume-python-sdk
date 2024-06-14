from __future__ import annotations

from hume import TranscriptionConfig


class TestTranscriptionConfig:
    def test_empty_serialize(self) -> None:
        config = TranscriptionConfig()
        assert config.to_dict() == {}

    def test_empty_deserialize(self) -> None:
        TranscriptionConfig.from_dict({})
