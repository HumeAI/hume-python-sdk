import json
import logging
from contextlib import asynccontextmanager
from typing import AsyncIterator, ClassVar, Optional

import websockets
import websockets.client

from hume._common.client_base import ClientBase
from hume._common.protocol import Protocol
from hume._voice.voice_socket import VoiceSocket
from hume.error.hume_client_exception import HumeClientException

logger = logging.getLogger(__name__)


class ChatMixin(ClientBase):
    DEFAULT_CUT_MS: ClassVar[int] = 250
    DEFAULT_ENCODING_NAME: ClassVar[str] = "linear16"
    DEFAULT_MAX_PAYLOAD_SIZE_BYTES: ClassVar[int] = 2**24
    DEFAULT_POSTPROCESS: ClassVar[bool] = True
    DEFAULT_SPEED_RATIO: ClassVar[float] = 1.2
    DEFAULT_TTS_TYPE: ClassVar[str] = "hume_ai"
    DEFAULT_LANGUAGE_MODEL_TYPE: ClassVar[str] = "claude-3-haiku-20240307"
    DEFAULT_LANGUAGE_MODEL_TEMPERATURE: ClassVar[float] = 0.7
    DEFAULT_GENERATE_SHORT_RESPONSE: ClassVar[bool] = False
    DEFAULT_NO_BINARY: ClassVar[bool] = False
    DEFAULT_SEND_GAP_MS: ClassVar[int] = -500
    DEFAULT_SENSITIVE_INTERRUPTIBILITY: ClassVar[bool] = False

    @asynccontextmanager
    async def connect(
        self,
        speed_ratio: float = DEFAULT_SPEED_RATIO,
        tts_type: str = DEFAULT_TTS_TYPE,
        config_id: Optional[str] = None,
        config_version: Optional[int] = None,
    ) -> AsyncIterator[VoiceSocket]:
        """Connect to the voice API."""
        uri_base = self._build_endpoint("evi", "chat", Protocol.WS)

        # TODO: Use proper query param formatting
        uri = (
            f"{uri_base}"
            f"?speed_ratio={speed_ratio}"
            f"&postprocess={json.dumps(self.DEFAULT_POSTPROCESS)}"
            f"&cut_ms={self.DEFAULT_CUT_MS}"
            f"&encoding={self.DEFAULT_ENCODING_NAME}"
            f"&channels={VoiceSocket.N_CHANNELS}"
            f"&sample_rate={VoiceSocket.SAMPLE_RATE}"
            f"&language_model_type={self.DEFAULT_LANGUAGE_MODEL_TYPE}"
            f"&language_model_temperature={self.DEFAULT_LANGUAGE_MODEL_TEMPERATURE}"
            f"&generate_short_response={json.dumps(self.DEFAULT_GENERATE_SHORT_RESPONSE)}"
            f"&no_binary={json.dumps(self.DEFAULT_NO_BINARY)}"
            f"&send_gap_ms={self.DEFAULT_SEND_GAP_MS}"
            f"&sensitive_interruptibility={json.dumps(self.DEFAULT_SENSITIVE_INTERRUPTIBILITY)}"
            f"&tts={tts_type}"
        )

        if config_id is not None:
            uri += f"&config_id={config_id}"
        if config_version is not None:
            uri += f"&config_version={config_version}"

        max_size = self.DEFAULT_MAX_PAYLOAD_SIZE_BYTES
        try:
            # pylint: disable=no-member
            async with websockets.connect(  # type: ignore[attr-defined]
                uri,
                extra_headers=self._get_client_headers(),
                close_timeout=self._close_timeout,
                open_timeout=self._open_timeout,
                max_size=max_size,
            ) as protocol:
                yield VoiceSocket(protocol)
        except websockets.exceptions.InvalidStatusCode as exc:
            status_code: int = exc.status_code
            if status_code == 401:  # Unauthorized
                message = "HumeVoiceClient initialized with invalid API key."
                raise HumeClientException(message) from exc
            raise HumeClientException("Unexpected error when creating voice API connection") from exc
