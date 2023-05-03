from hume import TranscriptionConfig


class TestTranscriptionConfig:

    def test_empty_serialize(self):
        config = TranscriptionConfig()
        assert config.to_dict() == {}

    def test_empty_deserialize(self):
        TranscriptionConfig.from_dict({})
