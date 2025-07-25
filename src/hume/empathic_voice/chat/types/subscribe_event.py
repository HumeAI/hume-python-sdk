# This file was auto-generated by Fern from our API Definition.

import typing

from ...types.assistant_end import AssistantEnd
from ...types.assistant_message import AssistantMessage
from ...types.assistant_prosody import AssistantProsody
from ...types.audio_output import AudioOutput
from ...types.chat_metadata import ChatMetadata
from ...types.tool_call_message import ToolCallMessage
from ...types.tool_error_message import ToolErrorMessage
from ...types.tool_response_message import ToolResponseMessage
from ...types.user_interruption import UserInterruption
from ...types.user_message import UserMessage
from ...types.web_socket_error import WebSocketError

SubscribeEvent = typing.Union[
    AssistantEnd,
    AssistantMessage,
    AssistantProsody,
    AudioOutput,
    ChatMetadata,
    WebSocketError,
    UserInterruption,
    UserMessage,
    ToolCallMessage,
    ToolResponseMessage,
    ToolErrorMessage,
]
