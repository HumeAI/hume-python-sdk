# This file was auto-generated by Fern from our API Definition.

from ...core.pydantic_utilities import UniversalBaseModel
import typing
import pydantic
from ...core.pydantic_utilities import IS_PYDANTIC_V2


class ReturnCustomVoiceParameters(UniversalBaseModel):
    """
    The specified attributes of a Custom Voice. If a parameter's value is `0` (default), it will not be included in the response.
    """

    gender: typing.Optional[int] = pydantic.Field(default=None)
    """
    The vocalization of gender, ranging between more masculine and more feminine.
    
    The default value is `0`, with a minimum of `-100` (more masculine) and a maximum of `100` (more feminine). A value of `0` leaves this parameter unchanged from the base voice.
    """

    articulation: typing.Optional[int] = pydantic.Field(default=None)
    """
    The clarity of the voice, ranging between mumbled and articulate.
    
    The default value is `0`, with a minimum of `-100` (mumbled) and a maximum of `100` (articulate). A value of `0` leaves this parameter unchanged from the base voice.
    """

    assertiveness: typing.Optional[int] = pydantic.Field(default=None)
    """
    The firmness of the voice, ranging between whiny and bold.
    
    The default value is `0`, with a minimum of `-100` (whiny) and a maximum of `100` (bold). A value of `0` leaves this parameter unchanged from the base voice.
    """

    buoyancy: typing.Optional[int] = pydantic.Field(default=None)
    """
    The density of the voice, ranging between deflated and buoyant.
    
    The default value is `0`, with a minimum of `-100` (deflated) and a maximum of `100` (buoyant). A value of `0` leaves this parameter unchanged from the base voice.
    """

    confidence: typing.Optional[int] = pydantic.Field(default=None)
    """
    The assuredness of the voice, ranging between shy and confident.
    
    The default value is `0`, with a minimum of `-100` (shy) and a maximum of `100` (confident). A value of `0` leaves this parameter unchanged from the base voice.
    """

    enthusiasm: typing.Optional[int] = pydantic.Field(default=None)
    """
    The excitement within the voice, ranging between calm and enthusiastic.
    
    The default value is `0`, with a minimum of `-100` (calm) and a maximum of `100` (enthusiastic). A value of `0` leaves this parameter unchanged from the base voice.
    """

    nasality: typing.Optional[int] = pydantic.Field(default=None)
    """
    The openness of the voice, ranging between clear and nasal.
    
    The default value is `0`, with a minimum of `-100` (clear) and a maximum of `100` (nasal). A value of `0` leaves this parameter unchanged from the base voice.
    """

    relaxedness: typing.Optional[int] = pydantic.Field(default=None)
    """
    The stress within the voice, ranging between tense and relaxed.
    
    The default value is `0`, with a minimum of `-100` (tense) and a maximum of `100` (relaxed). A value of `0` leaves this parameter unchanged from the base voice.
    """

    smoothness: typing.Optional[int] = pydantic.Field(default=None)
    """
    The texture of the voice, ranging between smooth and staccato.
    
    The default value is `0`, with a minimum of `-100` (smooth) and a maximum of `100` (staccato). A value of `0` leaves this parameter unchanged from the base voice.
    """

    tepidity: typing.Optional[int] = pydantic.Field(default=None)
    """
    The liveliness behind the voice, ranging between tepid and vigorous.
    
    The default value is `0`, with a minimum of `-100` (tepid) and a maximum of `100` (vigorous). A value of `0` leaves this parameter unchanged from the base voice.
    """

    tightness: typing.Optional[int] = pydantic.Field(default=None)
    """
    The containment of the voice, ranging between tight and breathy.
    
    The default value is `0`, with a minimum of `-100` (tight) and a maximum of `100` (breathy). A value of `0` leaves this parameter unchanged from the base voice.
    """

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
