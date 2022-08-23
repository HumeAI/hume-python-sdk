"""API type."""
from enum import Enum


class ApiType(Enum):
    """API type."""

    BATCH = "batch"
    STREAM = "stream"
