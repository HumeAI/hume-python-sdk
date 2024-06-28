# This file was auto-generated by Fern from our API Definition.

import datetime as dt
import typing

from ...core.datetime_utils import serialize_datetime
from ...core.pydantic_utilities import deep_union_pydantic_dicts, pydantic_v1
from .dataset_version import DatasetVersion


class ReturnDataset(pydantic_v1.BaseModel):
    id: typing.Optional[str] = pydantic_v1.Field(default=None)
    """
    Hume-generated Dataset ID
    """

    name: str = pydantic_v1.Field()
    """
    Dataset name
    """

    latest_version: typing.Optional[DatasetVersion] = None
    modified_on: typing.Optional[int] = pydantic_v1.Field(default=None)
    """
    Updated date and time
    """

    metadata: typing.Optional[typing.Dict[str, typing.Dict[str, typing.Any]]] = pydantic_v1.Field(default=None)
    """
    Additional details as key, value pairs
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
