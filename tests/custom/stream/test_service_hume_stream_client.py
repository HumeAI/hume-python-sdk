import re
from typing import Optional
from urllib.request import urlretrieve

import pytest
from pytest import TempPathFactory

from hume.client import HumeClient
from hume.core.api_error import ApiError
from hume.custom_models.types.language import Language
from hume.expression_measurement.stream.socket_client import AsyncStreamConnectOptions
from hume.expression_measurement.stream.types.stream_data_models import StreamDataModels
from hume.expression_measurement.stream.types.stream_data_models_face import StreamDataModelsFace
from hume.expression_measurement.stream.types.stream_data_models_language import StreamDataModelsLanguage
from hume.expression_measurement.types.face import Face
from hume.expression_measurement.types.facemesh_prediction import FacemeshPrediction
from hume.expression_measurement.types.prosody import Prosody
from utilities.eval_data import EvalData


@pytest.mark.asyncio
@pytest.mark.stream
@pytest.mark.service
class TestServiceHumeStreamClient:

    async def test_send_file(
        self,
        eval_data: EvalData,
        hume_client: HumeClient,
        tmp_path_factory: TempPathFactory,
    ) -> None:
        data_url = eval_data["image-obama-face"]
        data_filepath = tmp_path_factory.mktemp("data-dir") / "data-file"
        urlretrieve(data_url, data_filepath)

        async with hume_client.expression_measurement.stream.connect(
            options=AsyncStreamConnectOptions(
                config=StreamDataModels(face=StreamDataModelsFace(identify_faces=True))
            )
        ) as websocket:
            predictions = await websocket.send_file(data_filepath)
            assert predictions is not None

    async def test_send_text(self, hume_client: HumeClient) -> None:
        sample_text = "Hello! I hope this test works!"
        async with hume_client.expression_measurement.stream.connect(
            options=AsyncStreamConnectOptions(
                config=StreamDataModels(language=StreamDataModelsLanguage())
            )
        ) as websocket:
            predictions = await websocket.send_text(sample_text)
            assert predictions is not None

    async def test_send_facemesh(self, hume_client: HumeClient) -> None:
        meshes = [[[0.0, 0.0, 0.0]] * 478]
        async with hume_client.expression_measurement.stream.connect(
            options=AsyncStreamConnectOptions(config=StreamDataModels(facemesh={}))
        ) as websocket:
            predictions = await websocket.send_facemesh(landmarks=meshes)
            assert predictions is not None

    async def test_invalid_api_key(self) -> None:
        invalid_client = HumeClient(api_key="invalid-api-key")
        with pytest.raises(ApiError):
            async with invalid_client.expression_measurement.stream.connect(
                options=AsyncStreamConnectOptions(
                    config=StreamDataModels(face=StreamDataModelsFace(identify_faces=True))
                )
            ) as websocket:
                pass

    async def test_get_job_details(self, hume_client: HumeClient) -> None:
        async with hume_client.expression_measurement.stream.connect(
            options=AsyncStreamConnectOptions(
                config=StreamDataModels(prosody={})
            )
        ) as websocket:
            response = await websocket.get_job_details()
            job_id = response.job_details.job_id if response.job_details is not None else None
            assert job_id is not None
            if job_id is not None:
                assert len(job_id) == 32

    async def test_payload_config(
        self,
        eval_data: EvalData,
        hume_client: HumeClient,
        tmp_path_factory: TempPathFactory,
    ) -> None:
        data_dirpath = tmp_path_factory.mktemp("data-dir")
        face_data_url = eval_data["image-obama-face"]
        face_data_filepath = data_dirpath / "face-data-file"
        urlretrieve(face_data_url, face_data_filepath)
        text_data_url = eval_data["text-happy-place"]
        text_data_filepath = data_dirpath / "text-data-file"
        urlretrieve(text_data_url, text_data_filepath)

        async with hume_client.expression_measurement.stream.connect(
            options=AsyncStreamConnectOptions()
        ) as websocket:
            result = await websocket.send_file(
                face_data_filepath, config=StreamDataModels(face=StreamDataModelsFace())
            )
            assert result.face.predictions is not None # type: ignore
            result = await websocket.send_file(
                text_data_filepath, config=StreamDataModels(language=StreamDataModelsLanguage())
            )
            assert result.language.predictions is not None # type: ignore
