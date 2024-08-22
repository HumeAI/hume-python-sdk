# This file was auto-generated by Fern from our API Definition.

from ....core.pydantic_utilities import UniversalBaseModel
import typing
from .validation_args import ValidationArgs
from ....core.pydantic_utilities import IS_PYDANTIC_V2
import pydantic


class EvaluationArgs(UniversalBaseModel):
    validation: typing.Optional[ValidationArgs] = None

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
