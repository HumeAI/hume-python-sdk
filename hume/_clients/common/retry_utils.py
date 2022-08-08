import logging
import time
from typing import Any, Callable, Optional, TypeVar

from hume._clients.common.hume_client_error import HumeClientError

TRet = TypeVar('TRet')  # Return type of function being retried

logger = logging.getLogger(__name__)


class RetryIterError(Exception):
    pass


def retry(
    timeout: int = 300,
    backoff_factor: int = 2,
    error_type: Exception = RetryIterError,
):

    def decorator(func: Callable[[], Optional[TRet]]):

        def func_wrapper(*args: Any, **kwargs: Any):
            inner_timeout = timeout
            if "timeout" in kwargs:
                inner_timeout = kwargs["timeout"]
            inner_backoff_factor = backoff_factor
            if "backoff_factor" in kwargs:
                inner_backoff_factor = kwargs["backoff_factor"]

            delay = 1
            total_await_time = 0
            attempt = 1

            while True:
                logger.info(f"Retry attempt {attempt}, waited {total_await_time}s total")

                try:
                    return func(*args, **kwargs)
                except error_type as e:
                    logger.info(f"Retry iteration {attempt} failed: {str(e)}")

                if total_await_time >= inner_timeout:
                    raise HumeClientError(f"Request timed out after {inner_timeout}s")

                time.sleep(delay)
                total_await_time += delay

                new_delay = delay * inner_backoff_factor
                if total_await_time + new_delay > inner_timeout:
                    delay = inner_timeout - total_await_time
                else:
                    delay = new_delay

                attempt += 1

        return func_wrapper

    return decorator
