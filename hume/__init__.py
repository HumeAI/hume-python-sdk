"""Module init."""

from importlib.metadata import version

from hume._measurement.batch import (
    BatchJob,
    BatchJobDetails,
    BatchJobState,
    BatchJobStatus,
    HumeBatchClient,
    TranscriptionConfig,
)
from hume._measurement.stream import HumeStreamClient, StreamSocket
from hume._voice import HumeVoiceClient, MicrophoneInterface, VoiceChat, VoiceConfig, VoiceSocket
from hume.error.hume_client_exception import HumeClientException

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
    "MicrophoneInterface",
    "StreamSocket",
    "TranscriptionConfig",
    "VoiceChat",
    "VoiceConfig",
    "VoiceSocket",
]
