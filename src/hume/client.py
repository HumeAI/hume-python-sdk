# THIS FILE IS MANUALLY MAINTAINED: see .fernignore

import typing

import httpx

from .base_client import AsyncBaseHumeClient, BaseHumeClient

from .empathic_voice.socket_client import AsyncEmpathicVoiceClientWithWebsocket, EmpathicVoiceClientWithWebsocket
from .environment import HumeClientEnvironment
from .expression_measurement.socket_client import (
    AsyncExpressionMeasurementClientWithWebsocket,
    ExpressionMeasurementClientWithWebsocket
)


class HumeClient(BaseHumeClient):
    """
    Use this class to access the different functions within the SDK. You can instantiate any number of clients with different configuration that will propogate to these functions.

    Parameters
    ----------
    base_url : typing.Optional[str]
        The base url to use for requests from the client.

    environment : HumeClientEnvironment
        The environment to use for requests from the client. from .environment import HumeClientEnvironment



        Defaults to HumeClientEnvironment.PRODUCTION



    api_key : typing.Optional[str]
    timeout : typing.Optional[float]
        The timeout to be used, in seconds, for requests by default the timeout is 60 seconds, unless a custom httpx client is used, in which case a default is not set.

    follow_redirects : typing.Optional[bool]
        Whether the default httpx client follows redirects or not, this is irrelevant if a custom httpx client is passed in.

    httpx_client : typing.Optional[httpx.Client]
        The httpx client to use for making requests, a preconfigured client is used by default, however this is useful should you want to pass in any custom httpx configuration.

    Examples
    --------
    from hume.client import HumeClient

    client = HumeClient(
        api_key="YOUR_API_KEY",
    )
    """

    def __init__(
        self,
        *,
        base_url: typing.Optional[str] = None,
        environment: HumeClientEnvironment = HumeClientEnvironment.PRODUCTION,
        api_key: typing.Optional[str] = None,
        timeout: typing.Optional[float] = None,
        follow_redirects: typing.Optional[bool] = True,
        httpx_client: typing.Optional[httpx.Client] = None
    ):
        super().__init__(
            base_url=base_url,
            environment=environment,
            api_key=api_key,
            timeout=timeout,
            follow_redirects=follow_redirects,
            httpx_client=httpx_client,
        )
        self.empathic_voice: EmpathicVoiceClientWithWebsocket = (
            EmpathicVoiceClientWithWebsocket(client_wrapper=self._client_wrapper)
        )
        self.expression_measurement: ExpressionMeasurementClientWithWebsocket = (
            ExpressionMeasurementClientWithWebsocket(
                client_wrapper=self._client_wrapper
            )
        )


class AsyncHumeClient(AsyncBaseHumeClient):
    """
    Use this class to access the different functions within the SDK. You can instantiate any number of clients with different configuration that will propogate to these functions.
    Parameters
    ----------
    base_url : typing.Optional[str]
        The base url to use for requests from the client.
    environment : HumeClientEnvironment
        The environment to use for requests from the client. from .environment import HumeClientEnvironment
        Defaults to HumeClientEnvironment.PRODUCTION
    api_key : typing.Optional[str]
    timeout : typing.Optional[float]
        The timeout to be used, in seconds, for requests by default the timeout is 60 seconds, unless a custom httpx client is used, in which case a default is not set.
    follow_redirects : typing.Optional[bool]
        Whether the default httpx client follows redirects or not, this is irrelevant if a custom httpx client is passed in.
    httpx_client : typing.Optional[httpx.AsyncClient]
        The httpx client to use for making requests, a preconfigured client is used by default, however this is useful should you want to pass in any custom httpx configuration.
    Examples
    --------
    from hume.client import AsyncHumeClient
    client = AsyncHumeClient(
        api_key="YOUR_API_KEY",
    )
    """

    def __init__(
        self,
        *,
        base_url: typing.Optional[str] = None,
        environment: HumeClientEnvironment = HumeClientEnvironment.PRODUCTION,
        api_key: typing.Optional[str] = None,
        timeout: typing.Optional[float] = None,
        follow_redirects: typing.Optional[bool] = True,
        httpx_client: typing.Optional[httpx.AsyncClient] = None
    ):
        super().__init__(
            base_url=base_url,
            environment=environment,
            api_key=api_key,
            timeout=timeout,
            follow_redirects=follow_redirects,
            httpx_client=httpx_client,
        )
        self.empathic_voice: AsyncEmpathicVoiceClientWithWebsocket = (
            AsyncEmpathicVoiceClientWithWebsocket(client_wrapper=self._client_wrapper)
        )
        self.expression_measurement: AsyncExpressionMeasurementClientWithWebsocket = (
            AsyncExpressionMeasurementClientWithWebsocket(
                client_wrapper=self._client_wrapper
            )
        )
