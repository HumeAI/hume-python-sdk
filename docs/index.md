# Home

## Requirements

Python versions 3.9, 3.10, and 3.11 are supported

## Installation

Basic installation:

```bash
pip install hume
```

## Requirements

To use the basic functionality of `HumeVoiceClient`, `HumeBatchClient` or `HumeStreamClient` there are no additional system dependencies, however using the audio playback functionality of the EVI `MicrophoneInterface` may require a few extra dependencies depending on your operating system.

### Linux

- `libasound2-dev`
- `libportaudio2`

You can install these dependencies with:

```bash
sudo apt-get --yes update
sudo apt-get --yes install libasound2-dev libportaudio2
```

## Basic Usage

Jupyter example notebooks can be found in the [Python SDK GitHub repo](https://github.com/HumeAI/hume-python-sdk/tree/main/examples/README.md).

### Stream an EVI chat session

Start a new session using your device's microphone:

> Note: to use audio playback functionality in the MicrophoneInterface run `pip install hume[microphone]`

```python
import asyncio

from hume import HumeVoiceClient, MicrophoneInterface

async def main() -> None:
    client = HumeVoiceClient("<your-api-key>")

    async with client.connect() as socket:
        await MicrophoneInterface.start(socket)

asyncio.run(main())
```

Using a custom voice config:

```py
import asyncio

from hume import HumeVoiceClient, MicrophoneInterface

async def main() -> None:
    client = HumeVoiceClient("<your-api-key>")

    async with client.connect(config_id="<your-config-id>") as socket:
        await MicrophoneInterface.start(socket)

asyncio.run(main())
```

### Managing voice configs

Create a new config:

```py
from hume import HumeVoiceClient, VoiceConfig

client = HumeVoiceClient("<your-api-key">)
config: VoiceConfig = client.create_config(
    name=f"silly-poet",
    prompt="you are a silly poet",
)
print("Created config: ", config.id)
```

Get an existing config:

```py
from hume import HumeVoiceClient

client = HumeVoiceClient("<your-api-key">)
config = client.get_config("<YOUR CONFIG ID>")
print("Fetched config: ", config.name)
```

List all your configs:

```py
from hume import HumeVoiceClient

client = HumeVoiceClient("<your-api-key">)
for config in client.iter_configs():
    print(f"- {config.name} ({config.id})")
```

Delete a config:

```py
from hume import HumeVoiceClient

client = HumeVoiceClient("<your-api-key">)
client.delete_config("<YOUR CONFIG ID>")
```

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
