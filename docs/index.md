# Home

## Requirements

Python versions 3.9, 3.10, and 3.11 are supported

## Installation

Basic installation:

```bash
pip install hume
```

WebSocket and streaming features can be enabled with:

```bash
pip install "hume[stream]"
```

## Basic Usage

Jupyter example notebooks can be found in the [Python SDK GitHub repo](https://github.com/HumeAI/hume-python-sdk/tree/main/examples/README.md).

### Submit a new batch job

> Note: Your personal API key can be found in the profile section of [beta.hume.ai](https://beta.hume.ai)

```python
from hume import HumeBatchClient
from hume.models.config import FaceConfig
from hume.models.config import ProsodyConfig

client = HumeBatchClient("<your-api-key>")
urls = ["https://storage.googleapis.com/hume-test-data/video/armisen-clip.mp4"]
configs = [FaceConfig(identify_faces=True), ProsodyConfig()]
job = client.submit_job(urls, configs)

print(job)
print("Running...")

job.await_complete()
job.download_predictions("predictions.json")
print("Predictions downloaded to predictions.json")

job.download_artifacts("artifacts.zip")
print("Artifacts downloaded to artifacts.zip")
```

> Note: You can also supply a local filepath when submitting a batch job. Check it out in a Jupyter notebook [here](https://github.com/HumeAI/hume-python-sdk/tree/main/examples/batch-text-entity-recognition/batch-text-entity-recognition.ipynb).

### Rehydrate a batch job from a job ID

```python
from hume import HumeBatchClient

client = HumeBatchClient("<your-api-key>")

job_id = "<your-job-id>"
job = client.get_job(job_id)

print(job)
```

### Stream predictions over a WebSocket

> Note: `pip install "hume[stream]"` is required to use WebSocket features

```python
import asyncio

from hume import HumeStreamClient
from hume.models.config import BurstConfig
from hume.models.config import ProsodyConfig

async def main():
    client = HumeStreamClient("<your-api-key>")
    configs = [BurstConfig(), ProsodyConfig()]
    async with client.connect(configs) as socket:
        result = await socket.send_file("<your-audio-filepath>")
        print(result)

asyncio.run(main())
```

## Other Resources

- [Hume AI Homepage](https://hume.ai)
- [Platform Documentation](https://help.hume.ai/basics/about-hume-ai)
- [API Reference](https://streaming.hume.ai)

## Support

The Python SDK is open source! More details can be found on [GitHub](https://github.com/HumeAI/hume-python-sdk).

If you've found a bug with this SDK please [open an issue](https://github.com/HumeAI/hume-python-sdk/issues/new)!
