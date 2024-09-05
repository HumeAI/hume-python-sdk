import pytest
import aiofiles

from hume.client import AsyncHumeClient

# Get started with writing tests with pytest at https://docs.pytest.org
@pytest.mark.skip(reason="Unimplemented")
def test_client() -> None:
    assert True == True

@pytest.mark.skip(reason="CI does not have authentication.")
async def test_write_job_artifacts() -> None:
    client = AsyncHumeClient(api_key="MY_API_KEY")
    async with aiofiles.open('artifacts.zip', mode='wb') as file:
        async for chunk in client.expression_measurement.batch.get_job_artifacts(id="my-job-id"):
            await file.write(chunk)

@pytest.mark.skip(reason="CI does not have authentication.")
async def test_get_job_predictions() -> None:
    client = AsyncHumeClient(api_key="MY_API_KEY")
    await client.expression_measurement.batch.get_job_predictions(id="my-job-id", request_options={
        "max_retries": 3,
    })