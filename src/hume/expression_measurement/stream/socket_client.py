import base64
from contextlib import asynccontextmanager
import json
from pathlib import Path
import typing
import websockets
import websockets.protocol

from hume.core.api_error import ApiError

from ..stream.types.stream_data_models import StreamDataModels
from ..stream.types.subscribe_event import SubscribeEvent
from ...core.pydantic_utilities import pydantic_v1
from ...core.client_wrapper import AsyncClientWrapper


class AsyncStreamConnectOptions(pydantic_v1.BaseModel):
    config: typing.Optional[StreamDataModels] = None
    """
    Job config
    """

    config_version: typing.Optional[int] = None
    """
    Length of the sliding window in milliseconds to use when 
    aggregating media across streaming payloads within one WebSocket connection
    """

    api_key: typing.Optional[str] = None


class AsyncStreamWSSConnection:
    def __init__(
        self,
        *,
        websocket: websockets.WebSocketClientProtocol,
        params: AsyncStreamConnectOptions
    ):
        super().__init__()
        self.websocket = websocket
        self.params = params

    async def __aiter__(self):
        async for message in self.websocket:
            yield message

    # TODO: we can likely coerce the right response model within the union here, if we're
    # assuming request-response pattern and 1:1 mapping between request and response types
    async def _send(self, data: typing.Any) -> SubscribeEvent:
        await self.websocket.send(json.dumps(data))
        # Mimicing the request-reply pattern and waiting for the
        # response as soon as we send it
        return await self.recv()

    async def recv(self) -> SubscribeEvent:
        data = await self.websocket.recv()
        return pydantic_v1.parse_obj_as(SubscribeEvent, json.loads(data))  # type: ignore

    async def _send_config(
        self, data: str, raw_text: bool, config: typing.Optional[StreamDataModels]
    ) -> SubscribeEvent:
        if config != None:
            self.params.config = config

        to_send = {"data": data, "raw_text": raw_text}
        if self.params.config is not None:
            to_send["models"] = self.params.config.dict()

        return await self._send(to_send)

    async def get_job_details(self) -> SubscribeEvent:
        """
        Get details associated with the current streaming connection.

        Returns
        -------
        SubscribeEvent
        """
        return await self._send({"job_details": True})

    async def reset(self) -> SubscribeEvent:
        """
        Reset the streaming sliding window.

        A sliding window of context is maintained for the lifetime of your streaming
        connection. Call this method when some media has been fully processed and
        you want to continue using the same streaming connection without leaking context
        across media samples.

        Returns
        -------
        SubscribeEvent
        """
        return await self._send({"rese_stream": True})

    async def send_facemesh(
        self,
        landmarks: typing.List[typing.List[typing.List[float]]],
        config: typing.Optional[StreamDataModels] = None,
    ) -> SubscribeEvent:
        """
        Parameters
        ----------
        text : str
            List of landmark points for multiple faces. The shape of this 3-dimensional
            list should be (n, 478, 3) where n is the number of faces to be processed,
            478 is the number of MediaPipe landmarks per face and 3 represents the
            (x, y, z) coordinates of each landmark.

        config: typing.Optional[StreamDataModels]
            Model configurations. If set these configurations will overwrite any
            configurations set when initializing the StreamSocket.

        Returns
        -------
        SubscribeEvent
        """
        landmarks_str = json.dumps(landmarks)
        return await self._send_config(
            data=landmarks_str, raw_text=False, config=config
        )

    async def send_text(
        self, text: str, config: typing.Optional[StreamDataModels] = None
    ) -> SubscribeEvent:
        """
        Parameters
        ----------
        text : str
            Text to send to the language model.

        config: typing.Optional[StreamDataModels]
            Model configurations. If set these configurations will overwrite any
            configurations set when initializing the StreamSocket.

        Returns
        -------
        SubscribeEvent
        """
        return await self._send_config(data=text, raw_text=True, config=config)

    async def send_file(
        self, _file: typing.Union[str, Path], config: typing.Optional[StreamDataModels] = None
    ) -> SubscribeEvent:
        """
        Parameters
        ----------
        _file : str
            The path to the file to upload, or the Base64 encoded string of the file to upload.

        config: typing.Optional[StreamDataModels]
            Model configurations. If set these configurations will overwrite any
            configurations set when initializing the StreamSocket.

        Returns
        -------
        SubscribeEvent
        """

        try:
            with open(_file, "rb") as f:
                bytes_data = base64.b64encode(f.read()).decode()
        except:
            if isinstance(_file, Path): 
                raise ApiError(body=f"Failed to open file: {_file}")
            # If you cannot open the file, assume you were passed a b64 string, not a file path
            bytes_data = _file
    
        return await self._send_config(data=bytes_data, raw_text=False, config=config)


class AsyncStreamClientWithWebsocket:
    def __init__(self, *, client_wrapper: AsyncClientWrapper):
        self.client_wrapper = client_wrapper

    @asynccontextmanager
    async def connect(
        self, options: AsyncStreamConnectOptions
    ) -> typing.AsyncIterator[AsyncStreamWSSConnection]:
        api_key = options.api_key or self.client_wrapper.api_key
        if api_key is None:
            raise ValueError("An API key is required to connect to the streaming API.")
        
        try:
            async with websockets.connect(  # type: ignore[attr-defined]
                "wss://api.hume.ai/v0/stream/models",
                extra_headers={"X-Hume-Api-Key": api_key},
            ) as protocol:
                yield AsyncStreamWSSConnection(websocket=protocol, params=options)
        except websockets.exceptions.InvalidStatusCode as exc:
            status_code: int = exc.status_code
            if status_code == 401:
                raise ApiError(status_code=status_code, body="Websocket initialized with invalid credentials.") from exc
            raise ApiError(status_code=status_code, body="Unexpected error when initializing websocket connection.") from exc
