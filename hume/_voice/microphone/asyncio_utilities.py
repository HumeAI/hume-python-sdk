import dataclasses
from asyncio import Queue as BaseQueue
from typing import AsyncGenerator, AsyncIterator, Generic, TypeVar

T = TypeVar("T")


# NOTE: asyncio.Queue isn't itself async iterable
@dataclasses.dataclass
class Stream(Generic[T]):
    """Async iterable stream."""

    queue: BaseQueue
    agen: AsyncGenerator[T, None]

    @classmethod
    def new(cls) -> "Stream[T]":
        """Create a new async iterable stream."""
        return cls.from_queue(BaseQueue())

    @classmethod
    def from_queue(cls, queue: BaseQueue) -> "Stream[T]":
        """Create a new async iterable stream from a queue.

        Args:
            queue (asyncio.Queue): Queue to use for the stream.
        """
        return cls(queue=queue, agen=cls._agen(queue=queue))

    def __aiter__(self) -> AsyncIterator[T]:
        """Iterate over stream items."""
        return self.agen

    async def __anext__(self) -> T:
        """Get the next item in the stream."""
        return await self.agen.__anext__()

    @staticmethod
    async def _agen(*, queue: BaseQueue) -> AsyncGenerator[T, None]:
        while True:
            yield await queue.get()

    async def put(self, item: T) -> None:
        """Put an item into the stream."""
        await self.queue.put(item)

    async def aclose(self) -> None:
        """Close the stream."""
        await self.agen.aclose()
