"""Voice socket connection."""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any, AsyncIterator, ClassVar, List, Optional

from pydub import AudioSegment
from websockets.client import WebSocketClientProtocol as WebSocket

from hume._common.utilities.typing_utilities import JsonObject
from hume._voice.socket_inputs import (
    AssistantInput,
    AudioSettings,
    BuiltinToolConfig,
    PauseAssistantMessage,
    ResumeAssistantMessage,
    SessionSettings,
    TextUserInput,
    Tool,
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
    ) -> None:
        """Update the EVI session settings."""
        if num_channels is not None:
            self._num_channels = num_channels
        if sample_rate is not None:
            self._sample_rate = sample_rate

        session_settings = SessionSettings(
            custom_session_id=custom_session_id,
            type="session_settings",
            system_prompt=system_prompt,
            audio=AudioSettings(
                channels=num_channels,
                sample_rate=sample_rate,
            ),
            language_model_api_key=language_model_api_key,
            builtin_tools=builtin_tools,
            tools=tools,
        )

        settings_dict = session_settings.model_dump(exclude_none=True)

        logger.info(f"Updating session settings to: {settings_dict}")
        message = json.dumps(settings_dict)
        await self._protocol.send(message)

    async def send_file(self, filepath: Path) -> None:
        """Send a file over the voice socket.

        Args:
            filepath (Path): Filepath to the file to send over the socket.
        """
        with filepath.open("rb") as f:
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

    async def close(self) -> None:
        """Closes the underlying socket."""
        await self._protocol.close()
