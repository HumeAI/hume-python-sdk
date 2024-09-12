import base64
from contextlib import asynccontextmanager
import json
from pathlib import Path
import typing
import uuid
import websockets
import websockets.protocol

from hume.core.api_error import ApiError

from ..stream.types.config import Config
from ..stream.types.subscribe_event import SubscribeEvent
from ...core.pydantic_utilities import parse_obj_as
from ...core.client_wrapper import AsyncClientWrapper


class StreamConnectOptions(typing.TypedDict, total=False):
    api_key: typing.Optional[str]

    config: typing.Optional[Config]
    """
    Configuration used to specify which models should be used and with what settings.
    """


class StreamWebsocketConnection:
    def __init__(
        self,
        *,
        websocket: websockets.WebSocketClientProtocol,
        params: typing.Optional[StreamConnectOptions] = None,
        stream_window_ms: typing.Optional[float] = None,
    ):
        self.websocket = websocket
        self.params = params
        self.stream_window_ms = stream_window_ms

    async def __aiter__(self):
        async for message in self.websocket:
            yield parse_obj_as(SubscribeEvent, json.loads(message))  # type: ignore

    # TODO: we can likely coerce the right response model within the union here, if we're
    # assuming request-response pattern and 1:1 mapping between request and response types
    async def _send(self, data: typing.Any) -> SubscribeEvent:
        await self.websocket.send(json.dumps(data))
        # Mimicing the request-reply pattern and waiting for the
        # response as soon as we send it
        return await self.recv()

    async def recv(self) -> SubscribeEvent:
        data = await self.websocket.recv()
        return parse_obj_as(SubscribeEvent, json.loads(data))  # type: ignore

    async def _send_config(
        self,
        data: str,
        raw_text: bool,
        config: typing.Optional[Config],
        payload_id: typing.Optional[str] = None,
    ) -> SubscribeEvent:
        if config != None:
            if self.params is not None:
                self.params["config"] = config
            else:
                self.params = StreamConnectOptions(config=config)

        to_send = {
            "payload_id": payload_id or str(uuid.uuid4()),
            "data": data,
            "raw_text": raw_text,
        }
        if self.params is not None:
            config = self.params.get("config")
            if config is not None:
                to_send["models"] = config.dict()
        if self.stream_window_ms is not None:
            to_send["stream_window_ms"] = self.stream_window_ms

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
        return await self._send({"reset_stream": True})

    async def send_facemesh(
        self,
        landmarks: typing.List[typing.List[typing.List[float]]],
        config: typing.Optional[Config] = None,
        payload_id: typing.Optional[str] = None,
    ) -> SubscribeEvent:
        """
        Parameters
        ----------
        text : str
            List of landmark points for multiple faces. The shape of this 3-dimensional
            list should be (n, 478, 3) where n is the number of faces to be processed,
            478 is the number of MediaPipe landmarks per face and 3 represents the
            (x, y, z) coordinates of each landmark.

        config: typing.Optional[Config]
            Model configurations. If set these configurations will overwrite any
            configurations set when initializing the StreamSocket.

        Returns
        -------
        SubscribeEvent
        """
        landmarks_str = json.dumps(landmarks)
        return await self._send_config(
            data=landmarks_str, raw_text=False, config=config, payload_id=payload_id
        )

    async def send_text(
        self,
        text: str,
        config: typing.Optional[Config] = None,
        payload_id: typing.Optional[str] = None,
    ) -> SubscribeEvent:
        """
        Parameters
        ----------
        text : str
            Text to send to the language model.

        config: typing.Optional[Config]
            Model configurations. If set these configurations will overwrite any
            configurations set when initializing the StreamSocket.

        Returns
        -------
        SubscribeEvent
        """
        return await self._send_config(
            data=text, raw_text=True, config=config, payload_id=payload_id
        )

    async def send_file(
        self,
        file_: typing.Union[str, Path],
        config: typing.Optional[Config] = None,
        payload_id: typing.Optional[str] = None,
    ) -> SubscribeEvent:
        """
        Parameters
        ----------
        file_ : str
            The path to the file to upload, or the Base64 encoded string of the file to upload.

        config: typing.Optional[Config]
            Model configurations. If set these configurations will overwrite any
            configurations set when initializing the StreamSocket.

        Returns
        -------
        SubscribeEvent
        """

        try:
            with open(file_, "rb") as f:
                bytes_data = base64.b64encode(f.read()).decode()
        except:
            if isinstance(file_, Path):
                raise ApiError(body=f"Failed to open file: {file_}")
            # If you cannot open the file, assume you were passed a b64 string, not a file path
            bytes_data = file_

        return await self._send_config(
            data=bytes_data, raw_text=False, config=config, payload_id=payload_id
        )


class AsyncStreamClientWithWebsocket:
    def __init__(self, *, client_wrapper: AsyncClientWrapper):
        self.client_wrapper = client_wrapper

    @asynccontextmanager
    async def connect(
        self,
        options: typing.Optional[StreamConnectOptions] = None,
        stream_window_ms: typing.Optional[float] = None,
    ) -> typing.AsyncIterator[StreamWebsocketConnection]:
        api_key = (
            options.get("api_key")
            if options is not None and options.get("api_key")
            else self.client_wrapper.api_key
        )
        if api_key is None:
            raise ValueError("An API key is required to connect to the streaming API.")

        try:
            async with websockets.connect(  # type: ignore[attr-defined]
                "wss://api.hume.ai/v0/stream/models",
                extra_headers={
                    **self.client_wrapper.get_headers(include_auth=False),
                    "X-Hume-Api-Key": api_key,
                },
            ) as protocol:
                yield StreamWebsocketConnection(
                    websocket=protocol,
                    params=options,
                    stream_window_ms=stream_window_ms,
                )
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
