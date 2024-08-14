# Hume Python Library

[![fern shield](https://img.shields.io/badge/%F0%9F%8C%BF-SDK%20generated%20by%20Fern-brightgreen)](https://github.com/fern-api/fern)
[![pypi](https://img.shields.io/pypi/v/hume)](https://pypi.python.org/pypi/hume)

The Hume Python library provides convenient access to the Hume API from Python.

## Documentation & Examples

For complete documentation check out the [Python SDK docs site](https://humeai.github.io/hume-python-sdk/) or [try our quickstart guide](https://dev.hume.ai/docs/empathic-voice-interface-evi/quickstart/python).

Example notebooks can be found in the [examples folder](./examples/README.md).

## Other Resources

- [Hume AI Homepage](https://hume.ai)
- [Platform Documentation](https://dev.hume.ai)
- [API Reference](https://dev.hume.ai/reference)

## Citations

Hume's expressive communication platform has been built on top of published scientific research. If you use this SDK in your work please cite one of the relevant papers in [our publications repo](https://github.com/HumeAI/hume-research-publications).

## Installation

```sh
pip install hume
```

## Usage

Instantiate and use the client with the following:

```python
from hume import HumeClient

client = HumeClient(
    api_key="YOUR_API_KEY",
)
client.expression_measurement.batch.start_inference_job(
    urls=["https://hume-tutorials.s3.amazonaws.com/faces.zip"],
    notify=True,
)
```

## Async Client

The SDK also exports an `async` client so that you can make non-blocking calls to our API.

```python
import asyncio

from hume import AsyncHumeClient

client = AsyncHumeClient(
    api_key="YOUR_API_KEY",
)


async def main() -> None:
    await client.expression_measurement.batch.start_inference_job(
        urls=["https://hume-tutorials.s3.amazonaws.com/faces.zip"],
        notify=True,
    )


asyncio.run(main())
```

## Exception Handling

When the API returns a non-success status code (4xx or 5xx response), a subclass of the following error
will be thrown.

```python
from hume.core.api_error import ApiError

try:
    client.expression_measurement.batch.start_inference_job(...)
except ApiError as e:
    print(e.status_code)
    print(e.body)
```

## Pagination

Paginated requests will return a `SyncPager` or `AsyncPager`, which can be used as generators for the underlying object.

```python
from hume import HumeClient

client = HumeClient(
    api_key="YOUR_API_KEY",
)
response = client.empathic_voice.tools.list_tools(
    page_number=0,
    page_size=2,
)
for item in response:
    yield item
# alternatively, you can paginate page-by-page
for page in response.iter_pages():
    yield page
```

## Advanced

### Retries

The SDK is instrumented with automatic retries with exponential backoff. A request will be retried as long
as the request is deemed retriable and the number of retry attempts has not grown larger than the configured
retry limit (default: 2).

A request is deemed retriable when any of the following HTTP status codes is returned:

- [408](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/408) (Timeout)
- [429](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/429) (Too Many Requests)
- [5XX](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/500) (Internal Server Errors)

Use the `max_retries` request option to configure this behavior.

```python
client.expression_measurement.batch.start_inference_job(..., {
    "max_retries": 1
})
```

### Timeouts

The SDK defaults to a 60 second timeout. You can configure this with a timeout option at the client or request level.

```python

from hume import HumeClient

client = HumeClient(
    ...,
    timeout=20.0,
)


# Override timeout for a specific method
client.expression_measurement.batch.start_inference_job(..., {
    "timeout_in_seconds": 1
})
```

### Custom Client

You can override the `httpx` client to customize it for your use-case. Some common use-cases include support for proxies
and transports.
```python
import httpx
from hume import HumeClient

client = HumeClient(
    ...,
    httpx_client=httpx.Client(
        proxies="http://my.test.proxy.example.com",
        transport=httpx.HTTPTransport(local_address="0.0.0.0"),
    ),
)
```

## Contributing

While we value open-source contributions to this SDK, this library is generated programmatically.
Additions made directly to this library would have to be moved over to our generation code,
otherwise they would be overwritten upon the next generated release. Feel free to open a PR as
a proof of concept, but know that we will not be able to merge it as-is. We suggest opening
an issue first to discuss with us!

On the other hand, contributions to the README are always very welcome!
