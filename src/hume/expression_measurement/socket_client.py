from .client import AsyncExpressionMeasurementClient
from .stream.socket_client import AsyncStreamClientWithWebsocket


class AsyncExpressionMeasurementClientWithWebsocket(AsyncExpressionMeasurementClient):
    def __init__(self, *, client_wrapper):
        super().__init__(client_wrapper=client_wrapper)
        self.stream = AsyncStreamClientWithWebsocket(client_wrapper=client_wrapper)
