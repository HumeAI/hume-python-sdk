"""Module init."""

from importlib.metadata import version

from hume.legacy._measurement.batch import (
    BatchJob,
    BatchJobDetails,
    BatchJobState,
    BatchJobStatus,
    HumeBatchClient,
    TranscriptionConfig,
)
from hume.legacy._measurement.stream import HumeStreamClient, StreamSocket
from hume.legacy._voice import (
    HumeVoiceClient,
    LanguageModelConfig,
    MicrophoneInterface,
    VoiceChat,
    VoiceConfig,
    VoiceIdentityConfig,
    VoiceSocket,
    VoiceTool,
)
from hume.legacy.error.hume_client_exception import HumeClientException

__version__ = version("hume")

__all__ = [
    "__version__",
    "BatchJob",
    "BatchJobDetails",
    "BatchJobState",
    "BatchJobStatus",
    "HumeBatchClient",
    "HumeClientException",
    "HumeStreamClient",
    "HumeVoiceClient",
    "LanguageModelConfig",
    "MicrophoneInterface",
    "StreamSocket",
    "TranscriptionConfig",
    "VoiceChat",
    "VoiceConfig",
    "VoiceIdentityConfig",
    "VoiceSocket",
    "VoiceTool",
]
