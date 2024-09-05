import aiofiles
import typing

from ...core.request_options import RequestOptions

from .client import AsyncBatchClient, BatchClient

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