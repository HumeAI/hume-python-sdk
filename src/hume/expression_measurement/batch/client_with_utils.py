import aiofiles
import typing
import json as jsonlib
from json.decoder import JSONDecodeError

from ...core.request_options import RequestOptions
from ...core.jsonable_encoder import jsonable_encoder
from ... import core

from .types.inference_base_request import InferenceBaseRequest
from ...core.pydantic_utilities import parse_obj_as
from .types.job_id import JobId
from .client import AsyncBatchClient, BatchClient
from ...core.api_error import ApiError

class BatchClientWithUtils(BatchClient):
    def get_and_write_job_artifacts(
            self,
            id: str,
            *,
            file_name: str = "artifacts.zip",
            request_options: typing.Optional[RequestOptions] = None) -> None:
        """
        Get the artifacts ZIP of a completed inference job.

        Parameters
        ----------
        id : str
            The unique identifier for the job.

        file_name : typing.Optional[str]
            The name of the file to write the artifacts to.

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Yields
        ------
        typing.Iterator[bytes]


        Examples
        --------
        from hume.client import HumeClient

        client = HumeClient(
            api_key="YOUR_API_KEY",
        )
        client.expression_measurement.batch.get_and_write_job_artifacts(
            id="string",
            file_name="artifacts.zip",
        )
        """
        with open(file_name, mode='wb') as f:
            for chunk in self.get_job_artifacts(id=id, request_options=request_options):
                f.write(chunk)

    def start_inference_job_from_local_file(
        self,
        *,
        file: typing.List[core.File],
        json: typing.Optional[InferenceBaseRequest] = None,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> str:
        """
        Start a new batch inference job.

        Parameters
        ----------
        file : typing.List[core.File]
            See core.File for more documentation

        json : typing.Optional[InferenceBaseRequest]
            The inference job configuration.

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        str


        Examples
        --------
        from hume import HumeClient

        client = HumeClient(
            api_key="YOUR_API_KEY",
        )
        client.expression_measurement.batch.start_inference_job_from_local_file()
        """
        files: typing.Dict[str, typing.Any] = {
            "file": file,
        }
        if json is not None:
            files["json"] = jsonlib.dumps(jsonable_encoder(json)).encode("utf-8")

        _response = self._client_wrapper.httpx_client.request(
            "v0/batch/jobs",
            method="POST",
            files=files,
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                _parsed_response = typing.cast(
                    JobId,
                    parse_obj_as(
                        type_=JobId,  # type: ignore
                        object_=_response.json(),
                    ),
                )
                return _parsed_response.job_id
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)


class AsyncBatchClientWithUtils(AsyncBatchClient):
    async def get_and_write_job_artifacts(
            self,
            id: str,
            *,
            file_name: str = "artifacts.zip",
            request_options: typing.Optional[RequestOptions] = None) -> None:
        """
        Get the artifacts ZIP of a completed inference job.

        Parameters
        ----------
        id : str
            The unique identifier for the job.

        file_name : typing.Optional[str]
            The name of the file to write the artifacts to.

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Yields
        ------
        typing.AsyncIterator[bytes]


        Examples
        --------
        from hume.client import HumeClient

        client = AsyncHumeClient(
            api_key="YOUR_API_KEY",
        )
        await client.expression_measurement.batch.get_and_write_job_artifacts(
            id="string",
            file_name="artifacts.zip",
        )
        """
        async with aiofiles.open(file_name, mode='wb') as f:
            async for chunk in self.get_job_artifacts(id=id, request_options=request_options):
                await f.write(chunk)

    async def start_inference_job_from_local_file(
        self,
        *,
        file: typing.List[core.File],
        json: typing.Optional[InferenceBaseRequest] = None,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> str:
        """
        Start a new batch inference job.

        Parameters
        ----------
        file : typing.List[core.File]
            See core.File for more documentation

        json : typing.Optional[InferenceBaseRequest]
            The inference job configuration.

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        str


        Examples
        --------
        from hume import HumeClient

        client = HumeClient(
            api_key="YOUR_API_KEY",
        )
        client.expression_measurement.batch.start_inference_job_from_local_file()
        """
        files: typing.Dict[str, typing.Any] = {
            "file": file,
        }
        if json is not None:
            files["json"] = jsonlib.dumps(jsonable_encoder(json)).encode("utf-8")

        _response = await self._client_wrapper.httpx_client.request(
            "v0/batch/jobs",
            method="POST",
            files=files,
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                _parsed_response = typing.cast(
                    JobId,
                    parse_obj_as(
                        type_=JobId,  # type: ignore
                        object_=_response.json(),
                    ),
                )
                return _parsed_response.job_id
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)
