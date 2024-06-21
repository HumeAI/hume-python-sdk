"""Voice socket connection."""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any, AsyncIterator, ClassVar, List, Optional, Union

from pydub import AudioSegment
from websockets.client import WebSocketClientProtocol as WebSocket

from hume._common.utilities.typing_utilities import JsonObject
from hume._voice.socket_inputs import (
    AssistantInput,
    AudioSettings,
    BuiltinToolConfig,
    Context,
    PauseAssistantMessage,
    ResumeAssistantMessage,
    SessionSettings,
    TextUserInput,
    Tool,
    ToolErrorMessage,
    ToolResponseMessage,
)

logger = logging.getLogger(__name__)


class VoiceSocket:
    """Voice socket connection."""

    DEFAULT_CUT_MS: ClassVar[int] = 250
    DEFAULT_NUM_CHANNELS: ClassVar[int] = 1
    DEFAULT_SAMPLE_RATE: ClassVar[int] = 44_100

    def __init__(self, protocol: WebSocket):
        """Construct a `VoiceSocket`.

        Args:
            protocol (WebSocketClientProtocol): Protocol instance from websockets library.

        Raises:
            HumeClientException: If there is an error processing media over the socket connection.
        """
        self._protocol = protocol

        self._num_channels = self.DEFAULT_NUM_CHANNELS
        self._sample_rate = self.DEFAULT_SAMPLE_RATE

    async def __aiter__(self) -> AsyncIterator[Any]:
        """Async iterator for the voice socket."""
        async for message in self._protocol:
            yield message

    async def send(self, byte_str: bytes) -> None:
        """Send a byte string over the voice socket.

        Args:
            byte_str (bytes): Byte string to send.
        """
        await self._protocol.send(byte_str)

    async def send_json(self, message: JsonObject) -> None:
        """Send JSON as a byte string over the voice socket.

        Args:
            message (JsonObject): A dictionary representing a full JSON payload to the server.
        """
        await self._protocol.send(json.dumps(message).encode("utf-8"))

    async def recv(self) -> Any:
        """Receive a message on the voice socket."""
        await self._protocol.recv()

    async def update_session_settings(
        self,
        *,
        sample_rate: Optional[int] = None,
        num_channels: Optional[int] = None,
        custom_session_id: Optional[str] = None,
        system_prompt: Optional[str] = None,
        language_model_api_key: Optional[str] = None,
        builtin_tools: Optional[List[BuiltinToolConfig]] = None,
        tools: Optional[List[Tool]] = None,
        context_text: Optional[str] = None,
        context_type: Optional[str] = None,
    ) -> None:
        """
        Update the EVI session settings.

        This method allows updating various settings of the EVI session such as
        audio configurations, session ID, system prompt, API key for the language model,
        and tools configurations. If the number of channels or sample rate is specified,
        it updates the instance variables `_num_channels` and `_sample_rate` accordingly.

        Args:
            sample_rate (Optional[int]): The sample rate for audio data; updates session state variable if provided.
            num_channels (Optional[int]): The number of audio channels; updates session state variable if provided.
            custom_session_id (Optional[str]): A custom session ID to manage conversational state.
            context_text (Optional[str]): User context to inject.
            context_type (Optional[str]): The persistence level of the injected context. Allowed values include
            "editable", "persistent", and "temporary".
            system_prompt (Optional[str]): Instructions for how the system should respond to the user.
            Set to null to use the default system prompt.
            language_model_api_key (Optional[str]): Third party API key for the language model used for non-Hume models.
            builtin_tools (Optional[List[BuiltinToolConfig]]): List of built-in tool configurations session use.
            tools (Optional[List[Tool]]): List of custom tools configurations to be used in the session.

        Raises:
            HumeClientException: If there is an error processing media over the socket connection.
        """
        if num_channels is not None:
            self._num_channels = num_channels
        if sample_rate is not None:
            self._sample_rate = sample_rate

        context = None
        if context_text and context_type:
            context = Context(text=context_text, type=context_type)

        session_settings = SessionSettings(
            custom_session_id=custom_session_id,
            type="session_settings",
            system_prompt=system_prompt,
            audio=AudioSettings(
                channels=num_channels,
                sample_rate=sample_rate,
            ),
            context=context,
            language_model_api_key=language_model_api_key,
            builtin_tools=builtin_tools,
            tools=tools,
        )

        settings_dict = session_settings.model_dump(exclude_none=True)

        logger.info(f"Updating session settings to: {settings_dict}")
        message = json.dumps(settings_dict)
        await self._protocol.send(message)

    async def send_file(self, filepath: Union[str, Path]) -> None:
        """Send a file over the voice socket.

        Args:
            filepath (str | Path): Filepath to the file to send over the socket.
        """
        # Create a Path object from the filepath string
        path_object = Path(filepath)

        with path_object.open("rb") as f:
            segment: AudioSegment = AudioSegment.from_file(f)
            segment = segment.set_frame_rate(self._sample_rate).set_channels(self._num_channels)
            audio_bytes = segment.raw_data
            await self._protocol.send(audio_bytes)

    async def pause_assistant(self, custom_session_id: str | None = None) -> None:
        """Pause assistant.

        Args:
            custom_session_id (str, optional): Session ID for managing conversational state.
        """
        pause_assistant_message = PauseAssistantMessage(custom_session_id=custom_session_id)
        pause_assistant_message_dict = pause_assistant_message.model_dump(exclude_none=True)
        message = json.dumps(pause_assistant_message_dict)

        await self._protocol.send(message)

    async def resume_assistant(self, custom_session_id: str | None = None) -> None:
        """Resume assistant.

        Args:
            custom_session_id (str, optional): Session ID for managing conversational state.
        """
        resume_assistant_message = ResumeAssistantMessage(custom_session_id=custom_session_id)
        resume_assistant_message_dict = resume_assistant_message.model_dump(exclude_none=True)
        message = json.dumps(resume_assistant_message_dict)

        await self._protocol.send(message)

    async def send_assistant_input(self, input_text: str, custom_session_id: str | None = None) -> None:
        """Send assistant input.

        Args:
            text (str): Text to be synthesized.
            custom_session_id (str, optional): Session ID for managing conversational state.
        """
        assistant_input = AssistantInput(text=input_text, custom_session_id=custom_session_id)
        assistant_input_dict = assistant_input.model_dump(exclude_none=True)
        message = json.dumps(assistant_input_dict)

        await self._protocol.send(message)

    async def send_text_input(self, input_text: str, custom_session_id: str | None = None) -> None:
        """Send text input.

        Args:
            text (str): Text input to be sent.
            custom_session_id (str, optional): Session ID for managing conversational state.
        """
        text_user_input = TextUserInput(text=input_text, custom_session_id=custom_session_id)
        text_user_input_dict = text_user_input.model_dump(exclude_none=True)
        message = json.dumps(text_user_input_dict)

        await self._protocol.send(message)

    async def send_tool_response(
        self,
        content: str,
        tool_call_id: str,
        tool_type: str,
        custom_session_id: Optional[str] = None,
        tool_name: Optional[str] = None,
    ) -> None:
        """Send tool response.

        Args:
            content (str): Content of the tool response.
            tool_call_id (str): ID of the tool call.
            tool_type (str): Type of the tool, either 'builtin' or 'function'.
            custom_session_id (str, optional): Session ID for managing conversational state.
            tool_name (str, optional): Name of the tool.
        """
        tool_response = ToolResponseMessage(
            content=content,
            tool_call_id=tool_call_id,
            tool_type=tool_type,
            custom_session_id=custom_session_id,
            tool_name=tool_name,
        )
        tool_response_dict = tool_response.model_dump(exclude_none=True)
        message = json.dumps(tool_response_dict)

        await self._protocol.send(message)

    async def send_tool_error(
        self,
        error: str,
        tool_call_id: str,
        tool_type: str,
        custom_session_id: Optional[str] = None,
        code: Optional[str] = None,
        content: Optional[str] = None,
        level: Optional[str] = "warn",
    ) -> None:
        """Send tool error.

        Args:
            error (str): Error message.
            tool_call_id (str): ID of the tool call.
            tool_type (str): Type of the tool, either 'builtin' or 'function'.
            custom_session_id (str, optional): Session ID for managing conversational state.
            code (str, optional): Error code.
            content (str, optional): Content of the error message.
            level (str, optional): Error level.
        """
        tool_error = ToolErrorMessage(
            error=error,
            tool_call_id=tool_call_id,
            tool_type=tool_type,
            custom_session_id=custom_session_id,
            code=code,
            content=content,
            level=level,
        )
        tool_error_dict = tool_error.model_dump(exclude_none=True)
        message = json.dumps(tool_error_dict)

        await self._protocol.send(message)

    async def close(self) -> None:
        """Close the underlying socket."""
        await self._protocol.close()
