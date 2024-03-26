import dataclasses
from asyncio import Queue as BaseQueue
from typing import AsyncGenerator, AsyncIterator, Generic, TypeVar

T = TypeVar("T")


# NOTE: asyncio.Queue isn't itself async iterable
@dataclasses.dataclass
class Stream(Generic[T]):
    queue: BaseQueue
    agen: AsyncGenerator[T, None]

    @classmethod
    def new(cls) -> "Stream[T]":
        return cls.from_queue(BaseQueue())

    @classmethod
    def from_queue(cls, queue: BaseQueue) -> "Stream[T]":
        return cls(queue=queue, agen=cls._agen(queue=queue))

    def __aiter__(self) -> AsyncIterator[T]:
        return self.agen

    async def __anext__(self) -> T:
        return await self.agen.__anext__()

    @staticmethod
    async def _agen(*, queue: BaseQueue) -> AsyncGenerator[T, None]:
        while True:
            yield await queue.get()

    async def put(self, item: T) -> None:
        await self.queue.put(item)

    async def aclose(self) -> None:
        await self.agen.aclose()
