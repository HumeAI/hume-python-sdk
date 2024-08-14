# This file was auto-generated by Fern from our API Definition.

from ....core.pydantic_utilities import UniversalBaseModel
from .time_interval import TimeInterval
import typing
from .emotion_score import EmotionScore
import pydantic
from .descriptions_score import DescriptionsScore
from ....core.pydantic_utilities import IS_PYDANTIC_V2


class BurstPrediction(UniversalBaseModel):
    time: TimeInterval
    emotions: typing.List[EmotionScore] = pydantic.Field()
    """
    A high-dimensional embedding in emotion space.
    """

    descriptions: typing.List[DescriptionsScore] = pydantic.Field()
    """
    Modality-specific descriptive features and their scores.
    """

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
