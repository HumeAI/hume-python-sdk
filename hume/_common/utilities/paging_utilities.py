from typing import Optional

from hume._common.utilities.model_utilities import BaseModel


class Paging(BaseModel):
    page_size: Optional[int]
    page_number: int = 0
