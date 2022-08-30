# Hume Python SDK

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
