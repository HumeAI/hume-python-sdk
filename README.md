# Hume AI Python SDK

The Hume AI Python SDK makes it easy to call Hume APIs from Python applications.

To get started, [sign up for a Hume account](https://beta.hume.ai/sign-up)!

## Requirements

Python versions between 3.8 and 3.10 are supported

## Installation

```
pip install hume
```

## Example Usage

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
from hume import BatchJob, HumeBatchClient

client = HumeBatchClient("<your-api-key>")

job_id = "<your-job-id>"
job = BatchJob(client, job_id)

print(job)
```

## Documentation

Learn more about Hume's expressive communication platform on [our homepage](https://hume.ai) or our [platform docs](https://help.hume.ai/basics/about-hume-ai)

See example requests and responses for all available endpoints in the [Hume API Reference](https://docs.hume.ai)

## Support

If you've found a bug with this SDK please [open an issue](https://github.com/HumeAI/hume-python-sdk/issues/new)!
