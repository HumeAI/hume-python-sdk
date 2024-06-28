# This file was auto-generated by Fern from our API Definition.

import datetime as dt
import typing

from ...core.datetime_utils import serialize_datetime
from ...core.pydantic_utilities import deep_union_pydantic_dicts, pydantic_v1


class FileInput(pydantic_v1.BaseModel):
    """
    File details
    """

    name: str = pydantic_v1.Field()
    """
    File name
    """

    uri: typing.Optional[str] = pydantic_v1.Field(default=None)
    """
    File URI
    """

    hume_storage: bool = pydantic_v1.Field()
    """
    Flag which denotes whether the file is stored with Hume
    """

    data_type: str = pydantic_v1.Field()
    """
    File type: video, audio, video_no_audio, image, text, or mediapipe_facemesh
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