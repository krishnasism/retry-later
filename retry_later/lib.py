import asyncio
import inspect
import logging
import random
from collections.abc import Coroutine
from threading import Thread
from typing import Any, Callable, Union

from .types import ARGS_T, KWARGS_T, RT


async def awaitable_none() -> None:
    return None


def retry_later(
    retry_interval: int = 5,
    max_retries: int = 3,
    backoff: int = 1,
    exponential_backoff: bool = False,
    max_delay: int = -1,
    max_jitter: int = 0,
    exceptions: Union[type[Exception], tuple[type[Exception]]] = Exception,
) -> Callable[[Callable[..., RT]], Callable[..., RT]]:
    """Retry a function, later, in the background.

    Args:
        retry_interval (int): Time to wait in seconds between each retry. (Default: 5)
        max_retries (int): Maximum retries before giving up. (Default: 3)
        backoff (int): Multiplier to add between retry attempts. (Default: 1)
        exponential_backoff (bool): Flag to enable/disable exponential backoff. (Default: False)
        max_delay (int): Maximum delay. (Default: -1, no limit)
        max_jitter (int): Maximum random jitter. (Default: 0, no jitter)
        exceptions (Exception | tuple[Exception]): Exception or tuple of exceptions to retry.
            (Default: Exception Base class).
    Returns:
        None: No value is returned to the caller.
    """

    def decorator(func: Callable[..., RT]) -> Callable[..., Any]:
        async def wrapper(
            *args: ARGS_T,
            **kwargs: KWARGS_T,
        ) -> None:
            retries = 0
            jitter_range = range(0, max(0, max_jitter) + 1)
            while retries < max_retries:
                try:
                    if inspect.iscoroutinefunction(func):
                        await func(*args, **kwargs)
                    else:
                        func(*args, **kwargs)
                    return
                except exceptions as e:
                    retries += 1
                    if retries >= max_retries:
                        raise e
                    backoff_factor = backoff**retries if exponential_backoff else backoff
                    delay = retry_interval * backoff_factor + random.choice(jitter_range)
                    delay = delay if max_delay < 0 else min(max_delay, delay)
                    logging.error(f"[retry later] Retrying in {delay}s due to {e}")
                    await asyncio.sleep(delay)

        def callback(
            *args: ARGS_T,
            **kwargs: KWARGS_T,
        ) -> None:
            asyncio.run(wrapper(*args, **kwargs))

        def wrapper_threaded(
            *args: ARGS_T,
            **kwargs: KWARGS_T,
        ) -> Union[Coroutine[Any, Any, None], None]:
            Thread(target=callback, args=args, kwargs=kwargs, daemon=True).start()
            if inspect.iscoroutinefunction(func):
                return awaitable_none()
            return None

        return wrapper_threaded

    return decorator
