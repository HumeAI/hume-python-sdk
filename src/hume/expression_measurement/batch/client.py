# This file was auto-generated by Fern from our API Definition.

import typing
from json.decoder import JSONDecodeError

from ... import core
from ...core.api_error import ApiError
from ...core.client_wrapper import AsyncClientWrapper, SyncClientWrapper
from ...core.jsonable_encoder import jsonable_encoder
from ...core.pydantic_utilities import pydantic_v1
from ...core.request_options import RequestOptions
from ..types.direction import Direction
from ..types.inference_base_request import InferenceBaseRequest
from ..types.job_id import JobId
from ..types.models import Models
from ..types.sort_by import SortBy
from ..types.status import Status
from ..types.transcription import Transcription
from ..types.union_job import UnionJob
from ..types.union_predict_result import UnionPredictResult
from ..types.when import When

# this is used as the default value for optional parameters
OMIT = typing.cast(typing.Any, ...)


class BatchClient:
    def __init__(self, *, client_wrapper: SyncClientWrapper):
        self._client_wrapper = client_wrapper

    def list_jobs(
        self,
        *,
        limit: typing.Optional[int] = None,
        status: typing.Optional[typing.Union[Status, typing.Sequence[Status]]] = None,
        when: typing.Optional[When] = None,
        timestamp_ms: typing.Optional[int] = None,
        sort_by: typing.Optional[SortBy] = None,
        direction: typing.Optional[Direction] = None,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> typing.List[UnionJob]:
        """
        Sort and filter jobs.

        Parameters
        ----------
        limit : typing.Optional[int]
            The maximum number of jobs to include in the response.

        status : typing.Optional[typing.Union[Status, typing.Sequence[Status]]]
            Include only jobs of this status in the response. There are four possible statuses:

            - `QUEUED`: The job has been received and is waiting to be processed.

            - `IN_PROGRESS`: The job is currently being processed.

            - `COMPLETED`: The job has finished processing.

            - `FAILED`: The job encountered an error and could not be completed successfully.

        when : typing.Optional[When]
            Specify whether to include jobs created before or after a given `timestamp_ms`.

        timestamp_ms : typing.Optional[int]
            Provide a timestamp in milliseconds to filter jobs.

            When combined with the `when` parameter, you can filter jobs before or after the given timestamp. Defaults to the current Unix timestamp if one is not provided.

        sort_by : typing.Optional[SortBy]
            Specify which timestamp to sort the jobs by.

            - `created`: Sort jobs by the time of creation, indicated by `created_timestamp_ms`.

            - `started`: Sort jobs by the time processing started, indicated by `started_timestamp_ms`.

            - `ended`: Sort jobs by the time processing ended, indicated by `ended_timestamp_ms`.

        direction : typing.Optional[Direction]
            Specify the order in which to sort the jobs. Defaults to descending order.

            - `asc`: Sort in ascending order (chronological, with the oldest records first).

            - `desc`: Sort in descending order (reverse-chronological, with the newest records first).

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        typing.List[UnionJob]


        Examples
        --------
        from hume.client import HumeClient

        client = HumeClient(
            api_key="YOUR_API_KEY",
        )
        client.expression_measurement.batch.list_jobs()
        """
        _response = self._client_wrapper.httpx_client.request(
            "v0/batch/jobs",
            method="GET",
            params={
                "limit": limit,
                "status": status,
                "when": when,
                "timestamp_ms": jsonable_encoder(timestamp_ms),
                "sort_by": sort_by,
                "direction": direction,
            },
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                return pydantic_v1.parse_obj_as(typing.List[UnionJob], _response.json())  # type: ignore
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def start_inference_job(
        self,
        *,
        models: typing.Optional[Models] = OMIT,
        transcription: typing.Optional[Transcription] = OMIT,
        urls: typing.Optional[typing.Sequence[str]] = OMIT,
        registry_files: typing.Optional[typing.Sequence[str]] = OMIT,
        text: typing.Optional[typing.Sequence[str]] = OMIT,
        callback_url: typing.Optional[str] = OMIT,
        notify: typing.Optional[bool] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> JobId:
        """
        Start a new measurement inference job.

        Parameters
        ----------
        models : typing.Optional[Models]
            Specify the models to use for inference.

            If this field is not explicitly set, then all models will run by default.

        transcription : typing.Optional[Transcription]

        urls : typing.Optional[typing.Sequence[str]]
            URLs to the media files to be processed. Each must be a valid public URL to a media file (see recommended input filetypes) or an archive (`.zip`, `.tar.gz`, `.tar.bz2`, `.tar.xz`) of media files.

            If you wish to supply more than 100 URLs, consider providing them as an archive (`.zip`, `.tar.gz`, `.tar.bz2`, `.tar.xz`).

        registry_files : typing.Optional[typing.Sequence[str]]
            List of File IDs corresponding to the files in the asset registry.

        text : typing.Optional[typing.Sequence[str]]
            Text supplied directly to our Emotional Language and NER models for analysis.

        callback_url : typing.Optional[str]
            If provided, a `POST` request will be made to the URL with the generated predictions on completion or the error message on failure.

        notify : typing.Optional[bool]
            Whether to send an email notification to the user upon job completion/failure.

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        JobId


        Examples
        --------
        from hume.client import HumeClient

        client = HumeClient(
            api_key="YOUR_API_KEY",
        )
        client.expression_measurement.batch.start_inference_job(
            urls=["https://hume-tutorials.s3.amazonaws.com/faces.zip"],
            notify=True,
        )
        """
        _response = self._client_wrapper.httpx_client.request(
            "v0/batch/jobs",
            method="POST",
            json={
                "models": models,
                "transcription": transcription,
                "urls": urls,
                "registry_files": registry_files,
                "text": text,
                "callback_url": callback_url,
                "notify": notify,
            },
            request_options=request_options,
            omit=OMIT,
        )
        try:
            if 200 <= _response.status_code < 300:
                return pydantic_v1.parse_obj_as(JobId, _response.json())  # type: ignore
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def get_job_details(self, id: str, *, request_options: typing.Optional[RequestOptions] = None) -> UnionJob:
        """
        Get the request details and state of a given job.

        Parameters
        ----------
        id : str
            The unique identifier for the job.

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        UnionJob


        Examples
        --------
        from hume.client import HumeClient

        client = HumeClient(
            api_key="YOUR_API_KEY",
        )
        client.expression_measurement.batch.get_job_details(
            id="job_id",
        )
        """
        _response = self._client_wrapper.httpx_client.request(
            f"v0/batch/jobs/{jsonable_encoder(id)}", method="GET", request_options=request_options
        )
        try:
            if 200 <= _response.status_code < 300:
                return pydantic_v1.parse_obj_as(UnionJob, _response.json())  # type: ignore
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def get_job_predictions(
        self, id: str, *, request_options: typing.Optional[RequestOptions] = None
    ) -> typing.List[UnionPredictResult]:
        """
        Get the JSON predictions of a completed inference job.

        Parameters
        ----------
        id : str
            The unique identifier for the job.

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        typing.List[UnionPredictResult]


        Examples
        --------
        from hume.client import HumeClient

        client = HumeClient(
            api_key="YOUR_API_KEY",
        )
        client.expression_measurement.batch.get_job_predictions(
            id="job_id",
        )
        """
        _response = self._client_wrapper.httpx_client.request(
            f"v0/batch/jobs/{jsonable_encoder(id)}/predictions", method="GET", request_options=request_options
        )
        try:
            if 200 <= _response.status_code < 300:
                return pydantic_v1.parse_obj_as(typing.List[UnionPredictResult], _response.json())  # type: ignore
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def get_job_artifacts(
        self, id: str, *, request_options: typing.Optional[RequestOptions] = None
    ) -> typing.Iterator[bytes]:
        """
        Get the artifacts ZIP of a completed inference job.

        Parameters
        ----------
        id : str
            The unique identifier for the job.

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
        client.expression_measurement.batch.get_job_artifacts(
            id="string",
        )
        """
        with self._client_wrapper.httpx_client.stream(
            f"v0/batch/jobs/{jsonable_encoder(id)}/artifacts", method="GET", request_options=request_options
        ) as _response:
            try:
                if 200 <= _response.status_code < 300:
                    for _chunk in _response.iter_bytes():
                        yield _chunk
                    return
                _response.read()
                _response_json = _response.json()
            except JSONDecodeError:
                raise ApiError(status_code=_response.status_code, body=_response.text)
            raise ApiError(status_code=_response.status_code, body=_response_json)

    def start_inference_job_from_local_file(
        self,
        *,
        file: typing.List[core.File],
        json: typing.Optional[InferenceBaseRequest] = None,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> JobId:
        """
        Start a new batch inference job.

        Parameters
        ----------
        file : typing.List[core.File]
            See core.File for more documentation

        json : typing.Optional[InferenceBaseRequest]
            Stringified JSON object containing the inference job configuration.

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        JobId


        Examples
        --------
        from hume.client import HumeClient

        client = HumeClient(
            api_key="YOUR_API_KEY",
        )
        client.expression_measurement.batch.start_inference_job_from_local_file()
        """
        _response = self._client_wrapper.httpx_client.request(
            "v0/batch/jobs",
            method="POST",
            data={"json": json},
            files={"file": file},
            request_options=request_options,
            omit=OMIT,
        )
        try:
            if 200 <= _response.status_code < 300:
                return pydantic_v1.parse_obj_as(JobId, _response.json())  # type: ignore
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)


class AsyncBatchClient:
    def __init__(self, *, client_wrapper: AsyncClientWrapper):
        self._client_wrapper = client_wrapper

    async def list_jobs(
        self,
        *,
        limit: typing.Optional[int] = None,
        status: typing.Optional[typing.Union[Status, typing.Sequence[Status]]] = None,
        when: typing.Optional[When] = None,
        timestamp_ms: typing.Optional[int] = None,
        sort_by: typing.Optional[SortBy] = None,
        direction: typing.Optional[Direction] = None,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> typing.List[UnionJob]:
        """
        Sort and filter jobs.

        Parameters
        ----------
        limit : typing.Optional[int]
            The maximum number of jobs to include in the response.

        status : typing.Optional[typing.Union[Status, typing.Sequence[Status]]]
            Include only jobs of this status in the response. There are four possible statuses:

            - `QUEUED`: The job has been received and is waiting to be processed.

            - `IN_PROGRESS`: The job is currently being processed.

            - `COMPLETED`: The job has finished processing.

            - `FAILED`: The job encountered an error and could not be completed successfully.

        when : typing.Optional[When]
            Specify whether to include jobs created before or after a given `timestamp_ms`.

        timestamp_ms : typing.Optional[int]
            Provide a timestamp in milliseconds to filter jobs.

            When combined with the `when` parameter, you can filter jobs before or after the given timestamp. Defaults to the current Unix timestamp if one is not provided.

        sort_by : typing.Optional[SortBy]
            Specify which timestamp to sort the jobs by.

            - `created`: Sort jobs by the time of creation, indicated by `created_timestamp_ms`.

            - `started`: Sort jobs by the time processing started, indicated by `started_timestamp_ms`.

            - `ended`: Sort jobs by the time processing ended, indicated by `ended_timestamp_ms`.

        direction : typing.Optional[Direction]
            Specify the order in which to sort the jobs. Defaults to descending order.

            - `asc`: Sort in ascending order (chronological, with the oldest records first).

            - `desc`: Sort in descending order (reverse-chronological, with the newest records first).

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        typing.List[UnionJob]


        Examples
        --------
        import asyncio

        from hume.client import AsyncHumeClient

        client = AsyncHumeClient(
            api_key="YOUR_API_KEY",
        )


        async def main() -> None:
            await client.expression_measurement.batch.list_jobs()


        asyncio.run(main())
        """
        _response = await self._client_wrapper.httpx_client.request(
            "v0/batch/jobs",
            method="GET",
            params={
                "limit": limit,
                "status": status,
                "when": when,
                "timestamp_ms": jsonable_encoder(timestamp_ms),
                "sort_by": sort_by,
                "direction": direction,
            },
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                return pydantic_v1.parse_obj_as(typing.List[UnionJob], _response.json())  # type: ignore
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    async def start_inference_job(
        self,
        *,
        models: typing.Optional[Models] = OMIT,
        transcription: typing.Optional[Transcription] = OMIT,
        urls: typing.Optional[typing.Sequence[str]] = OMIT,
        registry_files: typing.Optional[typing.Sequence[str]] = OMIT,
        text: typing.Optional[typing.Sequence[str]] = OMIT,
        callback_url: typing.Optional[str] = OMIT,
        notify: typing.Optional[bool] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> JobId:
        """
        Start a new measurement inference job.

        Parameters
        ----------
        models : typing.Optional[Models]
            Specify the models to use for inference.

            If this field is not explicitly set, then all models will run by default.

        transcription : typing.Optional[Transcription]

        urls : typing.Optional[typing.Sequence[str]]
            URLs to the media files to be processed. Each must be a valid public URL to a media file (see recommended input filetypes) or an archive (`.zip`, `.tar.gz`, `.tar.bz2`, `.tar.xz`) of media files.

            If you wish to supply more than 100 URLs, consider providing them as an archive (`.zip`, `.tar.gz`, `.tar.bz2`, `.tar.xz`).

        registry_files : typing.Optional[typing.Sequence[str]]
            List of File IDs corresponding to the files in the asset registry.

        text : typing.Optional[typing.Sequence[str]]
            Text supplied directly to our Emotional Language and NER models for analysis.

        callback_url : typing.Optional[str]
            If provided, a `POST` request will be made to the URL with the generated predictions on completion or the error message on failure.

        notify : typing.Optional[bool]
            Whether to send an email notification to the user upon job completion/failure.

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        JobId


        Examples
        --------
        import asyncio

        from hume.client import AsyncHumeClient

        client = AsyncHumeClient(
            api_key="YOUR_API_KEY",
        )


        async def main() -> None:
            await client.expression_measurement.batch.start_inference_job(
                urls=["https://hume-tutorials.s3.amazonaws.com/faces.zip"],
                notify=True,
            )


        asyncio.run(main())
        """
        _response = await self._client_wrapper.httpx_client.request(
            "v0/batch/jobs",
            method="POST",
            json={
                "models": models,
                "transcription": transcription,
                "urls": urls,
                "registry_files": registry_files,
                "text": text,
                "callback_url": callback_url,
                "notify": notify,
            },
            request_options=request_options,
            omit=OMIT,
        )
        try:
            if 200 <= _response.status_code < 300:
                return pydantic_v1.parse_obj_as(JobId, _response.json())  # type: ignore
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    async def get_job_details(self, id: str, *, request_options: typing.Optional[RequestOptions] = None) -> UnionJob:
        """
        Get the request details and state of a given job.

        Parameters
        ----------
        id : str
            The unique identifier for the job.

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        UnionJob


        Examples
        --------
        import asyncio

        from hume.client import AsyncHumeClient

        client = AsyncHumeClient(
            api_key="YOUR_API_KEY",
        )


        async def main() -> None:
            await client.expression_measurement.batch.get_job_details(
                id="job_id",
            )


        asyncio.run(main())
        """
        _response = await self._client_wrapper.httpx_client.request(
            f"v0/batch/jobs/{jsonable_encoder(id)}", method="GET", request_options=request_options
        )
        try:
            if 200 <= _response.status_code < 300:
                return pydantic_v1.parse_obj_as(UnionJob, _response.json())  # type: ignore
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    async def get_job_predictions(
        self, id: str, *, request_options: typing.Optional[RequestOptions] = None
    ) -> typing.List[UnionPredictResult]:
        """
        Get the JSON predictions of a completed inference job.

        Parameters
        ----------
        id : str
            The unique identifier for the job.

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        typing.List[UnionPredictResult]


        Examples
        --------
        import asyncio

        from hume.client import AsyncHumeClient

        client = AsyncHumeClient(
            api_key="YOUR_API_KEY",
        )


        async def main() -> None:
            await client.expression_measurement.batch.get_job_predictions(
                id="job_id",
            )


        asyncio.run(main())
        """
        _response = await self._client_wrapper.httpx_client.request(
            f"v0/batch/jobs/{jsonable_encoder(id)}/predictions", method="GET", request_options=request_options
        )
        try:
            if 200 <= _response.status_code < 300:
                return pydantic_v1.parse_obj_as(typing.List[UnionPredictResult], _response.json())  # type: ignore
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    async def get_job_artifacts(
        self, id: str, *, request_options: typing.Optional[RequestOptions] = None
    ) -> typing.AsyncIterator[bytes]:
        """
        Get the artifacts ZIP of a completed inference job.

        Parameters
        ----------
        id : str
            The unique identifier for the job.

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Yields
        ------
        typing.AsyncIterator[bytes]


        Examples
        --------
        import asyncio

        from hume.client import AsyncHumeClient

        client = AsyncHumeClient(
            api_key="YOUR_API_KEY",
        )


        async def main() -> None:
            await client.expression_measurement.batch.get_job_artifacts(
                id="string",
            )


        asyncio.run(main())
        """
        async with self._client_wrapper.httpx_client.stream(
            f"v0/batch/jobs/{jsonable_encoder(id)}/artifacts", method="GET", request_options=request_options
        ) as _response:
            try:
                if 200 <= _response.status_code < 300:
                    async for _chunk in _response.aiter_bytes():
                        yield _chunk
                    return
                await _response.aread()
                _response_json = _response.json()
            except JSONDecodeError:
                raise ApiError(status_code=_response.status_code, body=_response.text)
            raise ApiError(status_code=_response.status_code, body=_response_json)

    async def start_inference_job_from_local_file(
        self,
        *,
        file: typing.List[core.File],
        json: typing.Optional[InferenceBaseRequest] = None,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> JobId:
        """
        Start a new batch inference job.

        Parameters
        ----------
        file : typing.List[core.File]
            See core.File for more documentation

        json : typing.Optional[InferenceBaseRequest]
            Stringified JSON object containing the inference job configuration.

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        JobId


        Examples
        --------
        import asyncio

        from hume.client import AsyncHumeClient

        client = AsyncHumeClient(
            api_key="YOUR_API_KEY",
        )


        async def main() -> None:
            await client.expression_measurement.batch.start_inference_job_from_local_file()


        asyncio.run(main())
        """
        _response = await self._client_wrapper.httpx_client.request(
            "v0/batch/jobs",
            method="POST",
            data={"json": json},
            files={"file": file},
            request_options=request_options,
            omit=OMIT,
        )
        try:
            if 200 <= _response.status_code < 300:
                return pydantic_v1.parse_obj_as(JobId, _response.json())  # type: ignore
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)
