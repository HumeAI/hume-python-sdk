import pytest
import aiofiles

from hume.client import AsyncHumeClient, HumeClient
from hume.expression_measurement.batch.types.face import Face
from hume.expression_measurement.batch.types.inference_base_request import InferenceBaseRequest
from hume.expression_measurement.batch.types.models import Models


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

# @pytest.mark.skip(reason="CI does not have authentication.")
async def test_start_inference_job_from_local_file() -> None:
    client = HumeClient(api_key="MY_API_KEY")
    client.expression_measurement.batch.start_inference_job_from_local_file(
        file=[],
        json=InferenceBaseRequest(
            models=Models(
                face=Face()
            )
        )
    )
