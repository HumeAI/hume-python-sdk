from __future__ import annotations

from hume.legacy._common.utilities.model_utilities import BaseModel


class Paging(BaseModel):
    """HTTP response paging parameters."""

    page_size: int | None
    page_number: int = 0
