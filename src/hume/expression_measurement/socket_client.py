from .client import AsyncExpressionMeasurementClient, ExpressionMeasurementClient
from .stream.socket_client import AsyncStreamClientWithWebsocket


class ExpressionMeasurementClientWithWebsocket(ExpressionMeasurementClient):
    def __init__(self, *, client_wrapper):
        super().__init__(client_wrapper=client_wrapper)
    
    @property
    def stream(self):
        raise NotImplementedError("The websocket at `.stream` is only available on the `AsyncHumeClient`, not this synchronous client (`HumeClient`).")

class AsyncExpressionMeasurementClientWithWebsocket(AsyncExpressionMeasurementClient):
    def __init__(self, *, client_wrapper):
        super().__init__(client_wrapper=client_wrapper)
        self.stream = AsyncStreamClientWithWebsocket(client_wrapper=client_wrapper)
