# This file was auto-generated by Fern from our API Definition.

from ....core.pydantic_utilities import UniversalBaseModel
import typing
from .stream_models_endpoint_payload_models import StreamModelsEndpointPayloadModels
import pydantic
from ....core.pydantic_utilities import IS_PYDANTIC_V2


class StreamModelsEndpointPayload(UniversalBaseModel):
    """
    Models endpoint payload
    """

    data: typing.Optional[str] = None
    models: typing.Optional[StreamModelsEndpointPayloadModels] = pydantic.Field(default=None)
    """
    Configuration used to specify which models should be used and with what settings.
    """

    stream_window_ms: typing.Optional[float] = pydantic.Field(default=None)
    """
    Length in milliseconds of streaming sliding window.
    
    Extending the length of this window will prepend media context from past payloads into the current payload.
    
    For example, if on the first payload you send 500ms of data and on the second payload you send an additional 500ms of data, a window of at least 1000ms will allow the model to process all 1000ms of stream data.
    
    A window of 600ms would append the full 500ms of the second payload to the last 100ms of the first payload.
    
    Note: This feature is currently only supported for audio data and audio models. For other file types and models this parameter will be ignored.
    """

    reset_stream: typing.Optional[bool] = pydantic.Field(default=None)
    """
    Whether to reset the streaming sliding window before processing the current payload.
    
    If this parameter is set to `true` then past context will be deleted before processing the current payload.
    
    Use reset_stream when one audio file is done being processed and you do not want context to leak across files.
    """

    raw_text: typing.Optional[bool] = pydantic.Field(default=None)
    """
    Set to `true` to enable the data parameter to be parsed as raw text rather than base64 encoded bytes.
    This parameter is useful if you want to send text to be processed by the language model, but it cannot be used with other file types like audio, image, or video.
    """

    job_details: typing.Optional[bool] = pydantic.Field(default=None)
    """
    Set to `true` to get details about the job.
    
    This parameter can be set in the same payload as data or it can be set without data and models configuration to get the job details between payloads.
    
    This parameter is useful to get the unique job ID.
    """

    payload_id: typing.Optional[str] = pydantic.Field(default=None)
    """
    Pass an arbitrary string as the payload ID and get it back at the top level of the socket response.
    
    This can be useful if you have multiple requests running asynchronously and want to disambiguate responses as they are received.
    """

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
