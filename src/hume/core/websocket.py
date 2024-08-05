import typing


OnOpenCloseHandlerType = typing.Union[typing.Callable[[], None], typing.Callable[[], typing.Awaitable[None]]]

MessageT = typing.TypeVar('MessageT')
OnMessageHandlerType = typing.Union[typing.Callable[[MessageT], None], typing.Callable[[MessageT], typing.Awaitable[None]]]

OnErrorHandlerType = typing.Union[typing.Callable[[Exception], None], typing.Callable[[Exception], typing.Awaitable[None]]]
