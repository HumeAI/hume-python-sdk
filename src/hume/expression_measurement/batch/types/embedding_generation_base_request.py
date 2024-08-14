# This file was auto-generated by Fern from our API Definition.

from ....core.pydantic_utilities import UniversalBaseModel
import typing
from .registry_file_detail import RegistryFileDetail
import pydantic
from ....core.pydantic_utilities import IS_PYDANTIC_V2


class EmbeddingGenerationBaseRequest(UniversalBaseModel):
    registry_file_details: typing.Optional[typing.List[RegistryFileDetail]] = pydantic.Field(default=None)
    """
    File ID and File URL pairs for an asset registry file
    """

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
