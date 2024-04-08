"""Protocol."""

from enum import Enum


class Protocol(str, Enum):
    """Protocol."""

    HTTP = "http"
    WS = "ws"
