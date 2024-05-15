from .chat.socket_client import AsyncChatClientWithWebsocket
from .client import AsyncEmpathicVoiceClient


class AsyncEmpathicVoiceClientWithWebsocket(AsyncEmpathicVoiceClient):
    def __init__(self, *, client_wrapper):
        super().__init__(client_wrapper=client_wrapper)
        self.chat = AsyncChatClientWithWebsocket(client_wrapper=client_wrapper)
