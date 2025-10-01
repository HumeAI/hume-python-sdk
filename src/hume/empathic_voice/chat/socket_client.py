# THIS FILE IS MANUALLY MAINTAINED: see .fernignore

import asyncio
import base64
from contextlib import asynccontextmanager
import json
import typing
import httpx
import websockets
import websockets.protocol
from json.decoder import JSONDecodeError

from hume.core.websocket import (
    OnErrorHandlerType,
    OnMessageHandlerType,
    OnOpenCloseHandlerType,
)
from hume.empathic_voice.chat.types.publish_event import PublishEvent
from hume.empathic_voice.types.context_type import ContextType
from hume.empathic_voice.types.pause_assistant_message import PauseAssistantMessage
from hume.empathic_voice.types.resume_assistant_message import ResumeAssistantMessage
from hume.empathic_voice.types.session_settings_variables_value import SessionSettingsVariablesValue
from hume.empathic_voice.types.tool_error_message import ToolErrorMessage
from hume.empathic_voice.types.tool_response_message import ToolResponseMessage

from ..chat.types.subscribe_event import SubscribeEvent
from ..types.assistant_input import AssistantInput
from ..types.session_settings import SessionSettings
from ..types.audio_input import AudioInput
from ..types.user_input import UserInput
from ...core.pydantic_utilities import parse_obj_as
from ...core.client_wrapper import AsyncClientWrapper
from ...core.api_error import ApiError



class ChatConnectSessionSettingsAudio(typing.TypedDict, total=False):
    channels: typing.Optional[int]
    encoding: typing.Optional[str]
    sample_rate: typing.Optional[int]


class ChatConnectSessionSettingsContext(typing.TypedDict, total=False):
    text: typing.Optional[str]
    type: ContextType


class ChatConnectSessionSettings(typing.TypedDict, total=False):
    audio: typing.Optional[ChatConnectSessionSettingsAudio]
    context: typing.Optional[ChatConnectSessionSettingsContext]
    custom_session_id: typing.Optional[str]
    event_limit: typing.Optional[int]
    language_model_api_key: typing.Optional[str]
    system_prompt: typing.Optional[str]
    variables: typing.Optional[typing.Dict[str, SessionSettingsVariablesValue]]
    voice_id: typing.Optional[str]


class ChatConnectOptions(typing.TypedDict, total=False):
    config_id: typing.Optional[str]
    """
    The ID of the configuration.
    """

    config_version: typing.Optional[str]
    """
    The version of the configuration.
    """

    api_key: typing.Optional[str]

    secret_key: typing.Optional[str]

    resumed_chat_group_id: typing.Optional[str]

    verbose_transcription: typing.Optional[bool]

    """
    ID of the Voice to use for this chat. If specified, will override the voice set in the Config
    """
    voice_id: typing.Optional[str]

    session_settings: typing.Optional[ChatConnectSessionSettings]
    """
    Session settings to apply at connection time. Supports all SessionSettings fields except
    builtin_tools, type, metadata, and tools. Additionally supports event_limit.
    """


class ChatWebsocketConnection:
    DEFAULT_NUM_CHANNELS: typing.ClassVar[int] = 1
    DEFAULT_SAMPLE_RATE: typing.ClassVar[int] = 44_100

    def __init__(
        self,
        *,
        websocket: websockets.WebSocketClientProtocol,
    ):
        self.websocket = websocket

        self._num_channels = self.DEFAULT_NUM_CHANNELS
        self._sample_rate = self.DEFAULT_SAMPLE_RATE

    async def __aiter__(self):
        async for message in self.websocket:
            yield parse_obj_as(SubscribeEvent, json.loads(message))  # type: ignore

    async def _send(self, data: typing.Any) -> None:
        if isinstance(data, dict):
            data = json.dumps(data)
        await self.websocket.send(data)

    async def recv(self) -> SubscribeEvent:
        data = await self.websocket.recv()
        return parse_obj_as(SubscribeEvent, json.loads(data))  # type: ignore

    async def _send_model(self, data: PublishEvent) -> None:
        await self._send(data.dict())

    async def send_audio_input(self, message: AudioInput) -> None:
        """
        Parameters
        ----------
        message : AudioInput

        Returns
        -------
        None
        """
        await self._send_model(message)

    async def send_session_settings(self, message: SessionSettings) -> None:
        """
        Update the EVI session settings.

        Parameters
        ----------
        message : SessionSettings

        Returns
        -------
        None
        """

        # Update sample rate and channels
        if message.audio is not None:
            if message.audio.channels is not None:
                self._num_channels = message.audio.channels
            if message.audio.sample_rate is not None:
                self._sample_rate = message.audio.sample_rate

        await self._send_model(message)

    async def send_user_input(self, message: UserInput) -> None:
        """
        Parameters
        ----------
        message : UserInput

        Returns
        -------
        None
        """
        await self._send_model(message)

    async def send_assistant_input(self, message: AssistantInput) -> None:
        """
        Parameters
        ----------
        message : AssistantInput

        Returns
        -------
        None
        """
        await self._send_model(message)

    async def send_tool_response(self, message: ToolResponseMessage) -> None:
        """
        Parameters
        ----------
        message : ToolResponseMessage

        Returns
        -------
        None
        """
        await self._send_model(message)

    async def send_tool_error(self, message: ToolErrorMessage) -> None:
        """
        Parameters
        ----------
        message : ToolErrorMessage

        Returns
        -------
        None
        """
        await self._send_model(message)

    async def send_pause_assistant(self, message: PauseAssistantMessage) -> None:
        """
        Parameters
        ----------
        message : PauseAssistantMessage

        Returns
        -------
        None
        """
        await self._send_model(message)

    async def send_resume_assistant(self, message: ResumeAssistantMessage) -> None:
        """
        Parameters
        ----------
        message : ResumeAssistantMessage

        Returns
        -------
        None
        """
        await self._send_model(message)


class AsyncChatClientWithWebsocket:
    DEFAULT_MAX_PAYLOAD_SIZE_BYTES: typing.ClassVar[int] = 2**24

    def __init__(self, *, client_wrapper: AsyncClientWrapper):
        self.client_wrapper = client_wrapper

    async def _construct_ws_uri(self, options: typing.Optional[ChatConnectOptions]):
        query_params = httpx.QueryParams()

        api_key = self.client_wrapper.api_key
        if options is not None:
            maybe_api_key = options.get("api_key")
            if maybe_api_key is not None:
                api_key = maybe_api_key
            maybe_config_id = options.get("config_id")
            if maybe_config_id is not None:
                query_params = query_params.add("config_id", maybe_config_id)
            maybe_config_version = options.get("config_version")
            if maybe_config_version is not None:
                query_params = query_params.add(
                    "config_version", maybe_config_version
                )
            maybe_resumed_chat_group_id = options.get("resumed_chat_group_id")
            if maybe_resumed_chat_group_id is not None:
                query_params = query_params.add(
                    "resumed_chat_group_id", maybe_resumed_chat_group_id
                )
            maybe_verbose_transcription = options.get("verbose_transcription")
            if maybe_verbose_transcription is not None:
                query_params = query_params.add(
                    "verbose_transcription",
                    "true" if maybe_verbose_transcription else "false",
                )
            maybe_secret_key = options.get("secret_key")
            if maybe_secret_key is not None and api_key is not None:
                query_params = query_params.add(
                    "accessToken",
                    await self._fetch_access_token(maybe_secret_key, api_key),
                )
            elif api_key is not None:
                query_params = query_params.add("apiKey", api_key)

            maybe_voice_id = options.get("voice_id")
            if maybe_voice_id is not None:
                query_params = query_params.add("voice_id", maybe_voice_id)

            maybe_session_settings = options.get("session_settings")
            if maybe_session_settings is not None:
                # Handle audio settings
                audio = maybe_session_settings.get("audio")
                if audio is not None:
                    channels = audio.get("channels")
                    if channels is not None:
                        query_params = query_params.add(
                            "session_settings[audio][channels]", str(channels)
                        )
                    encoding = audio.get("encoding")
                    if encoding is not None:
                        query_params = query_params.add(
                            "session_settings[audio][encoding]", str(encoding)
                        )
                    sample_rate = audio.get("sample_rate")
                    if sample_rate is not None:
                        query_params = query_params.add(
                            "session_settings[audio][sample_rate]", str(sample_rate)
                        )

                # Handle context settings
                context = maybe_session_settings.get("context")
                if context is not None:
                    text = context.get("text")
                    if text is not None:
                        query_params = query_params.add(
                            "session_settings[context][text]", str(text)
                        )
                    context_type = context.get("type")
                    if context_type is not None:
                        query_params = query_params.add(
                            "session_settings[context][type]", str(context_type)
                        )

                # Handle top-level session settings
                custom_session_id = maybe_session_settings.get("custom_session_id")
                if custom_session_id is not None:
                    query_params = query_params.add(
                        "session_settings[custom_session_id]", str(custom_session_id)
                    )

                event_limit = maybe_session_settings.get("event_limit")
                if event_limit is not None:
                    query_params = query_params.add(
                        "session_settings[event_limit]", str(event_limit)
                    )

                language_model_api_key = maybe_session_settings.get("language_model_api_key")
                if language_model_api_key is not None:
                    query_params = query_params.add(
                        "session_settings[language_model_api_key]", str(language_model_api_key)
                    )

                system_prompt = maybe_session_settings.get("system_prompt")
                if system_prompt is not None:
                    query_params = query_params.add(
                        "session_settings[system_prompt]", str(system_prompt)
                    )

                variables = maybe_session_settings.get("variables")
                if variables is not None:
                    query_params = query_params.add(
                        "session_settings[variables]", json.dumps(variables)
                    )

                voice_id_setting = maybe_session_settings.get("voice_id")
                if voice_id_setting is not None:
                    query_params = query_params.add(
                        "session_settings[voice_id]", str(voice_id_setting)
                    )
        elif api_key is not None:
            query_params = query_params.add("apiKey", api_key)

        base = self.client_wrapper.get_base_url().replace('https://', 'wss://').replace('http://', 'ws://')
        return f"{base}/v0/evi/chat?{query_params}"

    @asynccontextmanager
    async def connect(
        self, options: typing.Optional[ChatConnectOptions] = None
    ) -> typing.AsyncIterator[ChatWebsocketConnection]:
        ws_uri = await self._construct_ws_uri(options)

        try:
            async with websockets.connect(
                ws_uri,
                extra_headers=self.client_wrapper.get_headers(include_auth=False),
                max_size=self.DEFAULT_MAX_PAYLOAD_SIZE_BYTES,
            ) as protocol:
                yield ChatWebsocketConnection(websocket=protocol)
        except websockets.exceptions.InvalidStatusCode as exc:
            status_code: int = exc.status_code
            if status_code == 401:
                raise ApiError(
                    status_code=status_code,
                    body="Websocket initialized with invalid credentials.",
                ) from exc
            raise ApiError(
                status_code=status_code,
                body="Unexpected error when initializing websocket connection.",
            ) from exc

    async def _wrap_on_open_close(
        self, on_open: typing.Optional[OnOpenCloseHandlerType]
    ):
        if on_open is not None:
            if asyncio.iscoroutinefunction(on_open):
                await on_open()
            else:
                on_open()

    async def _wrap_on_error(
        self, exc: Exception, on_error: typing.Optional[OnErrorHandlerType]
    ) -> None:
        if on_error is not None:
            if asyncio.iscoroutinefunction(on_error):
                await on_error(exc)
            else:
                on_error(exc)

    async def _wrap_on_message(
        self,
        message: SubscribeEvent,
        on_message: typing.Optional[OnMessageHandlerType[SubscribeEvent]],
    ) -> None:
        if on_message is not None:
            if asyncio.iscoroutinefunction(on_message):
                await on_message(message)
            else:
                on_message(message)

    async def _process_connection(
        self,
        connection: ChatWebsocketConnection,
        on_message: typing.Optional[OnMessageHandlerType],
        on_error: typing.Optional[OnErrorHandlerType],
    ) -> None:
        async for message in connection:
            try:
                await self._wrap_on_message(message, on_message)
            except Exception as exc:
                await self._wrap_on_error(exc, on_error)

    @asynccontextmanager
    async def connect_with_callbacks(
        self,
        options: typing.Optional[ChatConnectOptions] = None,
        on_open: typing.Optional[OnOpenCloseHandlerType] = None,
        on_message: typing.Optional[OnMessageHandlerType[SubscribeEvent]] = None,
        on_close: typing.Optional[OnOpenCloseHandlerType] = None,
        on_error: typing.Optional[OnErrorHandlerType] = None,
    ) -> typing.AsyncIterator[ChatWebsocketConnection]:
        """
        Parameters
        ----------
        on_open : Optional[OnOpenCloseHandlerType]
            A callable to be invoked on the opening of the websocket connection.

        on_message : Optional[OnMessageHandlerType[SubscribeEvent]]
            A callable to be invoked on receiving a message from the websocket connection. This callback should expect a `SubscribeEvent` object.

        on_close : Optional[OnOpenCloseHandlerType]
            A callable to be invoked on the closing of the websocket connection.

        on_error : Optional[OnErrorHandlerType]
            A callable to be invoked on receiving an error from the websocket connection.

        Yields
        -------
        AsyncIterator[ChatWebsocketConnection]
        """

        ws_uri = await self._construct_ws_uri(options)
        background_task: typing.Optional[asyncio.Task[None]] = None

        try:
            async with websockets.connect(
                ws_uri,
                extra_headers=self.client_wrapper.get_headers(include_auth=False),
                max_size=self.DEFAULT_MAX_PAYLOAD_SIZE_BYTES,
            ) as protocol:
                await self._wrap_on_open_close(on_open)
                connection = ChatWebsocketConnection(websocket=protocol)
                background_task = asyncio.create_task(
                    self._process_connection(connection, on_message, on_error)
                )

                yield connection

        # Special case authentication errors
        except websockets.exceptions.InvalidStatusCode as exc:
            status_code: int = exc.status_code
            if status_code == 401:
                raise ApiError(
                    status_code=status_code,
                    body="Websocket initialized with invalid credentials.",
                ) from exc
            raise ApiError(
                status_code=status_code,
                body="Unexpected error when initializing websocket connection.",
            ) from exc

        # Except all other errors to apply the on_error handler
        except Exception as exc:
            await self._wrap_on_error(exc, on_error)
            raise

        # Finally, apply the on_close handler
        finally:
            if background_task is not None:
                background_task.cancel()
                try:
                    await background_task
                except asyncio.CancelledError:
                    pass
            await self._wrap_on_open_close(on_close)

    async def _fetch_access_token(self, secret_key: str, api_key: str) -> str:
        auth = f"{api_key}:{secret_key}"
        encoded_auth = base64.b64encode(auth.encode()).decode()
        _response = await self.client_wrapper.httpx_client.request(
            method="POST",
            base_url=self.client_wrapper.get_base_url(),
            path="oauth2-cc/token",
            headers={"Authorization": f"Basic {encoded_auth}"},
            data={"grant_type": "client_credentials"},
        )

        if 200 <= _response.status_code < 300:
            return _response.json()["access_token"]
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)
