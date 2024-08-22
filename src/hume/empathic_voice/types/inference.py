# This file was auto-generated by Fern from our API Definition.

from ...core.pydantic_utilities import UniversalBaseModel
import typing
from .prosody_inference import ProsodyInference
import pydantic
from ...core.pydantic_utilities import IS_PYDANTIC_V2


class Inference(UniversalBaseModel):
    prosody: typing.Optional[ProsodyInference] = pydantic.Field(default=None)
    """
    Prosody model inference results.
    
    EVI uses the prosody model to measure 48 emotions related to speech and vocal characteristics within a given expression.
    """

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
