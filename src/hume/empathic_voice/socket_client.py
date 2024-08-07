from .chat.socket_client import AsyncChatClientWithWebsocket
from .client import AsyncEmpathicVoiceClient, EmpathicVoiceClient


class EmpathicVoiceClientWithWebsocket(EmpathicVoiceClient):
    def __init__(self, *, client_wrapper):
        super().__init__(client_wrapper=client_wrapper)

    @property
    def chat(self) -> None:
        raise NotImplementedError("The websocket at `.chat` is only available on the `AsyncHumeClient`, not this synchronous client (`HumeClient`).")


class AsyncEmpathicVoiceClientWithWebsocket(AsyncEmpathicVoiceClient):
    def __init__(self, *, client_wrapper):
        super().__init__(client_wrapper=client_wrapper)
        self.chat = AsyncChatClientWithWebsocket(client_wrapper=client_wrapper)
