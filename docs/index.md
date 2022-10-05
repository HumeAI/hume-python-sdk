# Home

## Requirements

Python versions 3.8 and 3.9 are supported

## Installation

Basic installation:

```bash
$ pip install hume
```

Websocket and streaming features can be enabled with:

```bash
$ pip install hume[stream]
```

## Basic Usage

### Submit a new batch job

> Note: Your personal API key can be found in the profile section of [beta.hume.ai](https://beta.hume.ai)

```python
from hume import HumeBatchClient

client = HumeBatchClient("<your-api-key>")
urls = ["https://tinyurl.com/hume-img"]
job = client.submit_face(urls)

print(job)
print("Running...")

result = job.await_complete()
result.download_predictions("predictions.json")

print("Predictions downloaded!")
```

### Rehydrate a batch job from a job ID

```python
from hume import HumeBatchClient

client = HumeBatchClient("<your-api-key>")

job_id = "<your-job-id>"
job = client.get_job(job_id)

print(job)
```

### Stream predictions over a websocket

> Note: `pip install hume[stream]` is required to use websocket features

```python
import asyncio

from hume import HumeStreamClient, StreamSocket
from hume.config import FaceConfig

async def main():
    client = HumeStreamClient("<your-api-key>")
    configs = [FaceConfig(identify_faces=True)]
    async with client.connect(configs) as socket:
        socket: StreamSocket
        result = await socket.send_file("<your-image-filepath>")
        print(result)

asyncio.run(main())
```

## Other Resources

- [Hume AI Homepage](https://hume.ai)
- [Platform Documentation](https://help.hume.ai/basics/about-hume-ai)
- [API Reference](https://docs.hume.ai)

## Support

The Python SDK is open source! More details can be found on [GitHub](https://github.com/HumeAI/hume-python-sdk).

If you've found a bug with this SDK please [open an issue](https://github.com/HumeAI/hume-python-sdk/issues/new)!
