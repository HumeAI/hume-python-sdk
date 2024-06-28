# This file was auto-generated by Fern from our API Definition.

import datetime as dt
import typing

from ....core.datetime_utils import serialize_datetime
from ....core.pydantic_utilities import deep_union_pydantic_dicts, pydantic_v1
from .stream_job_details_job_details import StreamJobDetailsJobDetails


class StreamJobDetails(pydantic_v1.BaseModel):
    warning: typing.Optional[str] = pydantic_v1.Field(default=None)
    """
    Warning message text.
    """

    code: typing.Optional[str] = pydantic_v1.Field(default=None)
    """
    Unique identifier for the error.
    """

    payload_id: typing.Optional[str] = pydantic_v1.Field(default=None)
    """
    If a payload ID was passed in the request, the same payload ID will be sent back in the response body.
    """

    job_details: typing.Optional[StreamJobDetailsJobDetails] = pydantic_v1.Field(default=None)
    """
    If the job_details flag was set in the request, details about the current streaming job will be returned in the response body.
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
