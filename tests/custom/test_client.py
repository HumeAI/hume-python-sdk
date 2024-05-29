import os

import websockets

from hume.client import AsyncHumeClient, HumeClient
from hume.core.request_options import RequestOptions
from hume.empathic_voice.chat.socket_client import AsyncChatConnectOptions
from hume.empathic_voice.types.user_input import UserInput
from hume.expression_measurement.stream.socket_client import AsyncStreamConnectOptions
from hume.expression_measurement.stream.types.stream_data_models import StreamDataModels


# Get started with writing tests with pytest at https://docs.pytest.org
async def test_client() -> None:
    sync_hume = HumeClient()
    sync_hume.expression_measurement.batch.get_job_details("job_id", request_options=RequestOptions())

    for tool in sync_hume.empathic_voice.tools.list_tools():
        print(tool)

    hume = AsyncHumeClient(api_key=os.getenv("HUME_API_KEY"))
    async with hume.expression_measurement.stream.connect(
        options=AsyncStreamConnectOptions(config=StreamDataModels())
    ) as hwss:
        print(await hwss.get_job_details())

    async with hume.empathic_voice.chat.connect(
        options=AsyncChatConnectOptions(client_secret=os.getenv("HUME_CLIENT_SECRET"))
    ) as hwss:
        print(await hwss.send_text_input(message=UserInput(
            type="user_input",
            text="Hello, world!"
        )))

    job = hume.expression_measurement.batch_legacy.get_job("1")
    job.get_details()
