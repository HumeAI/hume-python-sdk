# This file was auto-generated by Fern from our API Definition.

import datetime as dt
import typing

from ...core.datetime_utils import serialize_datetime
from ...core.pydantic_utilities import deep_union_pydantic_dicts, pydantic_v1
from .posted_language_model_model_provider import PostedLanguageModelModelProvider


class PostedLanguageModel(pydantic_v1.BaseModel):
    """
    A LanguageModel to be posted to the server
    """

    model_provider: typing.Optional[PostedLanguageModelModelProvider] = pydantic_v1.Field(default=None)
    """
    The provider of the supplemental language model.
    """

    model_resource: typing.Optional[str] = pydantic_v1.Field(default=None)
    """
    String that specifies the language model to use with `model_provider`.
    """

    temperature: typing.Optional[float] = pydantic_v1.Field(default=None)
    """
    The model temperature, with values between 0 to 1 (inclusive).
    
    Controls the randomness of the LLM’s output, with values closer to 0 yielding focused, deterministic responses and values closer to 1 producing more creative, diverse responses.
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
