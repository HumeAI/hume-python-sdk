"""Protocol."""

from __future__ import annotations

from enum import Enum


class Protocol(str, Enum):
    """Protocol."""

    HTTP = "http"
    WS = "ws"
