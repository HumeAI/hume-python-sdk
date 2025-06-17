<div align="center">
  <img src="https://storage.googleapis.com/hume-public-logos/hume/hume-banner.png">
  <h1>Hume AI Python SDK</h1>

  <p>
    <strong>Integrate Hume APIs directly into your Python application</strong>
  </p>

  <br>
  <div>
    <a href="https://pypi.python.org/pypi/hume"><img src="https://img.shields.io/pypi/v/hume"></a>
    <a href="https://buildwithfern.com/"><img src="https://img.shields.io/badge/%F0%9F%8C%BF-SDK%20generated%20by%20Fern-brightgreen"></a>
  </div>
  <br>
</div>

## Migration Guide for Version 0.7.0 and Above

There were major breaking changes in version `0.7.0` of the SDK. If upgrading from a previous version, please 
**[View the Migration Guide](https://github.com/HumeAI/hume-python-sdk/wiki/Python-SDK-Migration-Guide)**. That release deprecated several interfaces and moved them to the `hume[legacy]` package extra. The `legacy` extra was removed in `0.9.0`. The last version to include `legacy` was `0.8.6`.

## Documentation

API reference documentation is available [here](https://dev.hume.ai/reference/).

## Compatibility

The Hume Python SDK is compatible across several Python versions and operating systems.

- For the [Empathic Voice Interface](https://dev.hume.ai/docs/empathic-voice-interface-evi/overview), Python versions `3.9` through `3.11` are supported on macOS and Linux.
- For [Text-to-speech (TTS)](https://dev.hume.ai/docs/text-to-speech-tts/overview), Python versions `3.9` through `3.12` are supported on macOS, Linux, and Windows.
- For [Expression Measurement](https://dev.hume.ai/docs/expression-measurement/overview), Python versions `3.9` through `3.12` are supported on macOS, Linux, and Windows.

Below is a table which shows the version and operating system compatibilities by product:

|                          | Python Version                | Operating System      |
| ------------------------ | ----------------------------- | --------------------- |
| Empathic Voice Interface | `3.9`, `3.10`, `3.11`         | macOS, Linux          |
| Text-to-speech (TTS)     | `3.9`, `3.10`, `3.11`, `3.12` | macOS, Linux, Windows |
| Expression Measurement   | `3.9`, `3.10`, `3.11`, `3.12` | macOS, Linux, Windows |

## Installation

```sh
pip install hume
# or
poetry add hume
# or
uv add hume
```

## Other Resources

```python
from hume.client import HumeClient

client = HumeClient(api_key="YOUR_API_KEY")
client.empathic_voice.configs.list_configs()
```

## Async Client

The SDK also exports an async client so that you can make non-blocking calls to our API.

```python
import asyncio

from hume.client import AsyncHumeClient

client = AsyncHumeClient(api_key="YOUR_API_KEY")

async def main() -> None:
    await client.empathic_voice.configs.list_configs()

asyncio.run(main())
```

### Writing File

Writing files with an async stream of bytes can be tricky in Python! `aiofiles` can simplify this some. For example,
you can download your job artifacts like so:

```python
import aiofiles

from hume import AsyncHumeClient

client = AsyncHumeClient()
async with aiofiles.open('artifacts.zip', mode='wb') as file:
    async for chunk in client.expression_measurement.batch.get_job_artifacts(id="my-job-id"):
        await file.write(chunk)
```

## Namespaces

This SDK contains the APIs for empathic voice, tts, and expression measurement. Even
if you do not plan on using more than one API to start, the SDK provides easy access in
case you would like to use additional APIs in the future.

Each API is namespaced accordingly:

```python
from hume.client import HumeClient

client = HumeClient(api_key="YOUR_API_KEY")

client.emapthic_voice.         # APIs specific to Empathic Voice
client.tts.                    # APIs specific to Text-to-speech
client.expression_measurement. # APIs specific to Expression Measurement
```

## Exception Handling

All errors thrown by the SDK will be subclasses of [`ApiError`](./src/hume/core/api_error.py).

```python
import hume.client

try:
  client.expression_measurement.batch.get_job_predictions(...)
except hume.core.ApiError as e: # Handle all errors
  print(e.status_code)
  print(e.body)
```

## Pagination

Paginated requests will return a `SyncPager` or `AsyncPager`, which can be used as generators for the underlying object. For example, `list_tools` will return a generator over `ReturnUserDefinedTool` and handle the pagination behind the scenes:

```python
import hume.client

client = HumeClient(api_key="YOUR_API_KEY")

for tool in client.empathic_voice.tools.list_tools():
  print(tool)
```

you could also iterate page-by-page:

```python
for page in client.empathic_voice.tools.list_tools().iter_pages():
  print(page.items)
```

or manually:

```python
pager = client.empathic_voice.tools.list_tools()
# First page
print(pager.items)
# Second page
pager = pager.next_page()
print(pager.items)
```

## WebSockets

We expose a websocket client for interacting with the EVI API as well as Expression Measurement.

When interacting with these clients, you can use them very similarly to how you'd use the common `websockets` library:

```python
from hume import StreamDataModels

client = AsyncHumeClient(api_key=os.getenv("HUME_API_KEY"))

async with client.expression_measurement.stream.connect(
    options={"config": StreamDataModels(...)}
) as hume_socket:
    print(await hume_socket.get_job_details())
```

The underlying connection, in this case `hume_socket`, will support intellisense/autocomplete for the different functions that are available on the socket!

### Advanced

#### Retries

The Hume SDK is instrumented with automatic retries with exponential backoff. A request will be
retried as long as the request is deemed retriable and the number of retry attempts has not grown larger
than the configured retry limit.

A request is deemed retriable when any of the following HTTP status codes is returned:

- [408](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/408) (Timeout)
- [409](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/409) (Conflict)
- [429](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/429) (Too Many Requests)
- [5XX](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/500) (Internal Server Errors)

Use the `max_retries` request option to configure this behavior.

```python
from hume.client import HumeClient
from hume.core import RequestOptions

client = HumeClient(...)

# Override retries for a specific method
client.expression_measurement.batch.get_job_predictions(...,
    request_options=RequestOptions(max_retries=5)
)
```

#### Timeouts

By default, requests time out after 60 seconds. You can configure this with a
timeout option at the client or request level.

```python
from hume.client import HumeClient
from hume.core import RequestOptions

client = HumeClient(
    # All timeouts are 20 seconds
    timeout=20.0,
)

# Override timeout for a specific method
client.expression_measurement.batch.get_job_predictions(...,
    request_options=RequestOptions(timeout_in_seconds=20)
)
```

#### Custom HTTP client

You can override the httpx client to customize it for your use-case. Some common use-cases
include support for proxies and transports.

```python
import httpx

from hume.client import HumeClient

client = HumeClient(
    http_client=httpx.Client(
        proxies="http://my.test.proxy.example.com",
        transport=httpx.HTTPTransport(local_address="0.0.0.0"),
    ),
)
```

## Contributing

While we value open-source contributions to this SDK, this library is generated programmatically.

Additions made directly to this library would have to be moved over to our generation code, otherwise they would be overwritten upon the next generated release. Feel free to open a PR as a proof of concept, but know that we will not be able to merge it as-is. We suggest opening an issue first to discuss with us!

On the other hand, contributions to the README are always very welcome!
