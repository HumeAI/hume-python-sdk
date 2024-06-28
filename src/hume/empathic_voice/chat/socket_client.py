import base64
from contextlib import asynccontextmanager
import json
import typing
import httpx
from pydub import AudioSegment
import websockets
import websockets.protocol
from json.decoder import JSONDecodeError
from pathlib import Path

from ..chat.types.subscribe_event import SubscribeEvent
from ..types.assistant_input import AssistantInput
from ..types.session_settings import SessionSettings
from ..types.audio_input import AudioInput
from ..types.user_input import UserInput
from ...core.pydantic_utilities import pydantic_v1
from ...core.client_wrapper import AsyncClientWrapper, SyncClientWrapper
from ...core.api_error import ApiError


class AsyncChatConnectOptions(pydantic_v1.BaseModel):
    config_id: typing.Optional[str] = None
    """
    The ID of the configuration.
    """

    config_version: typing.Optional[str] = None
    """
    The version of the configuration.
    """

    api_key: typing.Optional[str] = None

    client_secret: typing.Optional[str] = None


class AsyncChatWSSConnection:
    DEFAULT_NUM_CHANNELS: typing.ClassVar[int] = 1
    DEFAULT_SAMPLE_RATE: typing.ClassVar[int] = 44_100

    def __init__(
        self,
        *,
        websocket: websockets.WebSocketClientProtocol,
        params: AsyncChatConnectOptions,
    ):
        super().__init__()
        self.websocket = websocket
        self.params = params

        self._num_channels = self.DEFAULT_NUM_CHANNELS
        self._sample_rate = self.DEFAULT_SAMPLE_RATE

    async def __aiter__(self):
        async for message in self.websocket:
            yield message

    async def _send(self, data: typing.Any) -> SubscribeEvent:
        if isinstance(data, dict):
            data = json.dumps(data)
        await self.websocket.send(data)
        # Mimicing the request-reply pattern and waiting for the
        # response as soon as we send it
        return await self.recv()

    async def recv(self) -> SubscribeEvent:
        data = await self.websocket.recv()
        return pydantic_v1.parse_obj_as(SubscribeEvent, json.loads(data))  # type: ignore

    async def send_audio_input(self, message: AudioInput) -> SubscribeEvent:
        """
        Parameters
        ----------
        message : AudioInput

        Returns
        -------
        SubscribeEvent
        """
        return await self._send(message.dict())

    async def send_session_settings(self, message: SessionSettings) -> SubscribeEvent:
        """
        Update the EVI session settings.

        Parameters
        ----------
        message : SessionSettings

        Returns
        -------
        SubscribeEvent
        """

        # Update sample rate and channels
        if message.audio is not None:
            if message.audio.channels is not None:
                self._num_channels = message.audio.channels
            if message.audio.sample_rate is not None:
                self._sample_rate = message.audio.sample_rate

        return await self._send(message.dict())

    async def send_text_input(self, message: UserInput) -> SubscribeEvent:
        """
        Parameters
        ----------
        message : UserInput

        Returns
        -------
        SubscribeEvent
        """
        return await self._send(message.dict())

    async def send_assistant_input(self, message: AssistantInput) -> SubscribeEvent:
        """
        Parameters
        ----------
        message : AssistantInput

        Returns
        -------
        SubscribeEvent
        """
        return await self._send(message.dict())
    
    async def send_file(self, filepath: Path) -> None:
        """Send a file over the voice socket.

        Parameters
        ----------
        filepath : Path
            Filepath to the file to send over the socket.
        """
        with filepath.open("rb") as f:
            segment: AudioSegment = AudioSegment.from_file(f)  # type: ignore
            segment = segment.set_frame_rate(self._sample_rate).set_channels(self._num_channels)
            audio_bytes = segment.raw_data
            await self._send(audio_bytes)


class AsyncChatClientWithWebsocket:
    def __init__(self, *, client_wrapper: typing.Union[AsyncClientWrapper, SyncClientWrapper]):
        self.client_wrapper = client_wrapper

    @asynccontextmanager
    async def connect(
        self, options: AsyncChatConnectOptions
    ) -> typing.AsyncIterator[AsyncChatWSSConnection]:
        query_params = httpx.QueryParams()

        api_key = options.api_key or self.client_wrapper.api_key

        if options.config_id is not None:
            query_params = query_params.add("config_id", options.config_id)
        if options.config_version is not None:
            query_params = query_params.add("config_version", options.config_version)
        
        if options.client_secret is not None and api_key is not None:
            query_params = query_params.add(
                "accessToken",
                await self._fetch_access_token(options.client_secret, api_key),
            )
        elif api_key is not None:
            query_params = query_params.add("apiKey", api_key)

        ws_uri = f"wss://api.hume.ai/v0/evi/chat?{query_params}"

        try:
            async with websockets.connect(ws_uri) as protocol:
                yield AsyncChatWSSConnection(websocket=protocol, params=options)
        except websockets.exceptions.InvalidStatusCode as exc:
            status_code: int = exc.status_code
            if status_code == 401:
                raise ApiError(status_code=status_code, body="Websocket initialized with invalid credentials.") from exc
            raise ApiError(status_code=status_code, body="Unexpected error when initializing websocket connection.") from exc


    async def _fetch_access_token(self, client_secret: str, api_key: str) -> str:
        auth = f"{api_key}:{client_secret}"
        encoded_auth = base64.b64encode(auth.encode()).decode()
        if isinstance(self.client_wrapper.httpx_client, httpx.AsyncClient):
            _response = await self.client_wrapper.httpx_client.request(
                method="POST",
                url="https://api.hume.ai/oauth2-cc/token",
                headers={"Authorization": f"Basic {encoded_auth}"},
                data={"grant_type": "client_credentials"},
            )
        else:
            _response = await self.client_wrapper.httpx_client.request(   # type: ignore
                method="POST",
                url="https://api.hume.ai/oauth2-cc/token",
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