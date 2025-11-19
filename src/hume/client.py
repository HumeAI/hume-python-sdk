# THIS FILE IS MANUALLY MAINTAINED: see .fernignore

import typing

import httpx

from .base_client import AsyncBaseHumeClient, BaseHumeClient

from .environment import HumeClientEnvironment


def _base_url_to_environment(base_url: str) -> HumeClientEnvironment:
    if base_url.startswith("http://"):
        return HumeClientEnvironment(
            base=base_url,
            evi=base_url.replace("http://", "ws://") + "/v0/evi",
            tts=base_url.replace("http://", "ws://") + "/v0/tts",
            stream=base_url.replace("http://", "ws://") + "/v0/stream",
        )
    elif base_url.startswith("https://"):
        return HumeClientEnvironment(
            base=base_url,
            evi=base_url.replace("https://", "wss://") + "/v0/evi",
            tts=base_url.replace("https://", "wss://") + "/v0/tts",
            stream=base_url.replace("https://", "wss://") + "/v0/stream",
        )
    else:
        # Assume https if no protocol specified
        return HumeClientEnvironment(
            base="https://" + base_url,
            evi="wss://" + base_url + "/v0/evi",
            tts="wss://" + base_url + "/v0/tts",
            stream="wss://" + base_url + "/v0/stream",
        )


class HumeClient(BaseHumeClient):
    """
    Use this class to access the different functions within the SDK. You can instantiate any number of clients with different configuration that will propogate to these functions.

    Parameters
    ----------
    base_url : typing.Optional[str]
        The base URL to use for requests from the client. If provided, this will be converted
        to a HumeClientEnvironment. Can be a full URL (http://... or https://...) or just
        a hostname (which will default to https://).
    environment : typing.Optional[HumeClientEnvironment]
        The environment to use for requests from the client. from .environment import HumeClientEnvironment
        Defaults to None, which will use HumeClientEnvironment.PROD. Cannot be specified together with base_url.
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
        environment: typing.Optional[HumeClientEnvironment] = None,
        api_key: typing.Optional[str] = None,
        headers: typing.Optional[typing.Dict[str, str]] = None,
        timeout: typing.Optional[float] = None,
        follow_redirects: typing.Optional[bool] = True,
        httpx_client: typing.Optional[httpx.Client] = None
    ):
        # Error if both base_url and environment are specified
        if base_url is not None and environment is not None:
            raise ValueError("Cannot specify both 'base_url' and 'environment'. Please use only one.")
        
        # Convert base_url string to environment if provided
        if base_url is not None:
            environment = _base_url_to_environment(base_url)
        
        # Default to PROD if neither base_url nor environment was provided
        if environment is None:
            environment = HumeClientEnvironment.PROD
        
        super().__init__(
            environment=environment,
            api_key=api_key,
            headers=headers,
            timeout=timeout,
            follow_redirects=follow_redirects,
            httpx_client=httpx_client,
        )


class AsyncHumeClient(AsyncBaseHumeClient):
    """
    Use this class to access the different functions within the SDK. You can instantiate any number of clients with different configuration that will propogate to these functions.
    Parameters
    ----------
    base_url : typing.Optional[str]
        The base URL to use for requests from the client. If provided, this will be converted
        to a HumeClientEnvironment. Can be a full URL (http://... or https://...) or just
        a hostname (which will default to https://).
    environment : typing.Optional[HumeClientEnvironment]
        The environment to use for requests from the client. from .environment import HumeClientEnvironment
        Defaults to None, which will use HumeClientEnvironment.PROD. Cannot be specified together with base_url.
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
        environment: typing.Optional[HumeClientEnvironment] = None,
        headers: typing.Optional[typing.Dict[str, str]] = None,
        api_key: typing.Optional[str] = None,
        timeout: typing.Optional[float] = None,
        follow_redirects: typing.Optional[bool] = True,
        httpx_client: typing.Optional[httpx.AsyncClient] = None
    ):
        # Error if both base_url and environment are specified
        if base_url is not None and environment is not None:
            raise ValueError("Cannot specify both 'base_url' and 'environment'. Please use only one.")
        
        # Convert base_url string to environment if provided
        if base_url is not None:
            environment = _base_url_to_environment(base_url)
        
        # Default to PROD if neither base_url nor environment was provided
        if environment is None:
            environment = HumeClientEnvironment.PROD
        
        super().__init__(
            environment=environment,
            api_key=api_key,
            headers=headers,
            timeout=timeout,
            follow_redirects=follow_redirects,
            httpx_client=httpx_client,
        )
