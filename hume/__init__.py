"""Module init."""
import importlib.metadata

from hume._batch import BatchJob, BatchJobResult, BatchJobStatus, HumeBatchClient
from hume._stream import HumeStreamClient, StreamSocket
from hume._common.hume_client_exception import HumeClientException
from hume._common.model_type import ModelType

__version__ = importlib.metadata.version("hume")

__all__ = [
    "__version__",
    "BatchJob",
    "BatchJobResult",
    "BatchJobStatus",
    "HumeBatchClient",
    "HumeClientException",
    "HumeStreamClient",
    "ModelType",
    "StreamSocket",
]
