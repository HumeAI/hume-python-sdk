"""Module init."""
from importlib.metadata import version

from hume._batch import BatchJob, BatchJobInfo, BatchJobStatus, HumeBatchClient, TranscriptionConfig
from hume._stream import HumeStreamClient, StreamSocket
from hume.error.hume_client_exception import HumeClientException

__version__ = version("hume")

__all__ = [
    "__version__",
    "BatchJob",
    "BatchJobInfo",
    "BatchJobStatus",
    "HumeBatchClient",
    "HumeClientException",
    "HumeStreamClient",
    "StreamSocket",
    "TranscriptionConfig",
]
