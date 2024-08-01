# This file was auto-generated by Fern from our API Definition.

import datetime as dt
import typing

from ...core.datetime_utils import serialize_datetime
from ...core.pydantic_utilities import deep_union_pydantic_dicts, pydantic_v1
from .models import Models
from .transcription import Transcription


class InferenceBaseRequest(pydantic_v1.BaseModel):
    models: typing.Optional[Models] = None
    transcription: typing.Optional[Transcription] = None
    urls: typing.Optional[typing.List[str]] = pydantic_v1.Field(default=None)
    """
    URLs to the media files to be processed. Each must be a valid public URL to a media file (see recommended input filetypes) or an archive (`.zip`, `.tar.gz`, `.tar.bz2`, `.tar.xz`) of media files.
    
    If you wish to supply more than 100 URLs, consider providing them as an archive (`.zip`, `.tar.gz`, `.tar.bz2`, `.tar.xz`).
    """

    registry_files: typing.Optional[typing.List[str]] = pydantic_v1.Field(default=None)
    """
    List of File IDs corresponding to the files in the asset registry.
    """

    text: typing.Optional[typing.List[str]] = pydantic_v1.Field(default=None)
    """
    Text to supply directly to our language and NER models.
    """

    callback_url: typing.Optional[str] = pydantic_v1.Field(default=None)
    """
    If provided, a `POST` request will be made to the URL with the generated predictions on completion or the error message on failure.
    """

    notify: typing.Optional[bool] = pydantic_v1.Field(default=None)
    """
    Whether to send an email notification to the user upon job completion/failure.
    """

    def json(self, **kwargs: typing.Any) -> str:
        kwargs_with_defaults: typing.Any = {"by_alias": True, "exclude_unset": True, **kwargs}
        return super().json(**kwargs_with_defaults)

    def dict(self, **kwargs: typing.Any) -> typing.Dict[str, typing.Any]:
        kwargs_with_defaults_exclude_unset: typing.Any = {"by_alias": True, "exclude_unset": True, **kwargs}
        kwargs_with_defaults_exclude_none: typing.Any = {"by_alias": True, "exclude_none": True, **kwargs}

        return deep_union_pydantic_dicts(
            super().dict(**kwargs_with_defaults_exclude_unset), super().dict(**kwargs_with_defaults_exclude_none)
        )

    class Config:
        frozen = True
        smart_union = True
        extra = pydantic_v1.Extra.allow
        json_encoders = {dt.datetime: serialize_datetime}
