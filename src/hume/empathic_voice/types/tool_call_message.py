# This file was auto-generated by Fern from our API Definition.

from ...core.pydantic_utilities import UniversalBaseModel
import typing
import pydantic
from .tool_type import ToolType
from ...core.pydantic_utilities import IS_PYDANTIC_V2


class ToolCallMessage(UniversalBaseModel):
    """
    When provided, the output is a tool call.
    """

    custom_session_id: typing.Optional[str] = pydantic.Field(default=None)
    """
    Used to manage conversational state, correlate frontend and backend data, and persist conversations across EVI sessions.
    """

    name: str = pydantic.Field()
    """
    Name of the tool called.
    """

    parameters: str = pydantic.Field()
    """
    Parameters of the tool.
    
    These parameters define the inputs needed for the tool’s execution, including the expected data type and description for each input field. Structured as a stringified JSON schema, this format ensures the tool receives data in the expected format.
    """

    response_required: bool = pydantic.Field()
    """
    Indicates whether a response to the tool call is required from the developer, either in the form of a [Tool Response message](/reference/empathic-voice-interface-evi/chat/chat#send.Tool%20Response%20Message.type) or a [Tool Error message](/reference/empathic-voice-interface-evi/chat/chat#send.Tool%20Error%20Message.type).
    """

    tool_call_id: str = pydantic.Field()
    """
    The unique identifier for a specific tool call instance.
    
    This ID is used to track the request and response of a particular tool invocation, ensuring that the correct response is linked to the appropriate request.
    """

    tool_type: typing.Optional[ToolType] = pydantic.Field(default=None)
    """
    Type of tool called. Either `builtin` for natively implemented tools, like web search, or `function` for user-defined tools.
    """

    type: typing.Literal["tool_call"] = pydantic.Field(default="tool_call")
    """
    The type of message sent through the socket; for a Tool Call message, this must be `tool_call`.
    
    This message indicates that the supplemental LLM has detected a need to invoke the specified tool.
    """

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
