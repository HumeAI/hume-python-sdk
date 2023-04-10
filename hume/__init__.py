"""Module init."""
import importlib.metadata

from hume._batch import BatchJob, BatchJobResult, BatchJobStatus, HumeBatchClient
from hume._stream import HumeStreamClient, StreamSocket
from hume.error.hume_client_exception import HumeClientException

__version__ = importlib.metadata.version("hume")

__all__ = [
    "__version__",
    "BatchJob",
    "BatchJobResult",
    "BatchJobStatus",
    "HumeBatchClient",
    "HumeClientException",
    "HumeStreamClient",
    "StreamSocket",
]
