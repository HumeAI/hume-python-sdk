"""Module init."""
from importlib.metadata import version

from hume._batch import BatchJob, BatchJobResult, BatchJobStatus, HumeBatchClient, TranscriptionConfig
from hume._stream import HumeStreamClient, StreamSocket
from hume.error.hume_client_exception import HumeClientException

__version__ = version("hume")

__all__ = [
    "__version__",
    "BatchJob",
    "BatchJobResult",
    "BatchJobStatus",
    "HumeBatchClient",
    "HumeClientException",
    "HumeStreamClient",
    "StreamSocket",
    "TranscriptionConfig",
]
