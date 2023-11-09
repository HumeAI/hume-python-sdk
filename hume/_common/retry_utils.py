"""Function retry utilities."""
import logging
import time
from typing import Callable, Optional, Type, TypeVar, cast

from typing_extensions import ParamSpec

from hume.error.hume_client_exception import HumeClientException

P = ParamSpec("P")  # Parameter type variable for decorated function
R = TypeVar("R")  # Return type variable for decorated function

logger = logging.getLogger(__name__)


class RetryIterError(Exception):
    """Retry iteration exception.

    Raised when a job has not completed by the allotted timeout.
    """


def retry(
    timeout: int = 300,
    max_delay: int = 300,
    backoff_factor: int = 2,
    error_type: Type[Exception] = RetryIterError,
    timeout_message: Optional[str] = None,
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """Retry decorator for exponential backoff retry.

    Args:
        timeout (int): Maximum seconds to keep retrying before giving up. Defaults to 300.
        max_delay (int): Maximum seconds to delay between retries. Defaults to 300.
        backoff_factor (int): Multiplier factor for exponential backoff. Defaults to 2.
        error_type (Type[Exception]): Class of exception to expect from decorated function when
            the function fails. Raise this exception type if the retry iteration has failed.
            Defaults to RetryIterError.
        timeout_message (Optional[str]): A message that will be used when raising a
            HumeClientException on timeout.

    Returns:
        Callable[[Callable[P, R]], Callable[P, R]]: Function decorator.
    """

    def decorator_func(decorated_func: Callable[P, R]) -> Callable[P, R]:
        def func_wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            # If the decorated function has kwargs that match the retry decorator kwargs,
            # then those values override the retry kwargs.
            retry_kwargs = {
                "timeout": timeout,
                "max_delay": max_delay,
                "backoff_factor": backoff_factor,
            }
            for retry_var in retry_kwargs:
                if retry_var in kwargs:
                    retry_kwargs[retry_var] = cast(int, kwargs[retry_var])

            delay = 1
            total_await_time = 0
            attempt = 1

            while True:
                logger.info(f"Retry attempt {attempt}, waited {total_await_time}s total")

                try:
                    return decorated_func(*args, **kwargs)
                except error_type as exc:
                    logger.info(f"Retry iteration {attempt} failed: {str(exc)}")

                retry_timeout = retry_kwargs["timeout"]
                if total_await_time >= retry_timeout:
                    message = timeout_message
                    if timeout_message is None:
                        message = f"Request timed out after {retry_timeout}s"
                    raise HumeClientException(message)

                time.sleep(delay)
                total_await_time += delay

                new_delay = delay * retry_kwargs["backoff_factor"]

                # Avoid going over the max delay
                if new_delay > retry_kwargs["max_delay"]:
                    new_delay = retry_kwargs["max_delay"]

                # Avoid going over the total timeout
                if total_await_time + new_delay > retry_timeout:
                    delay = retry_timeout - total_await_time
                else:
                    delay = new_delay

                attempt += 1

        return func_wrapper

    return decorator_func
