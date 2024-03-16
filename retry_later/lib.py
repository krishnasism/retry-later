import asyncio
import inspect
import logging
import random
from threading import Thread
from typing import Callable, Union


def retry_later(
    retry_interval: int = 5,
    max_retries: int = 3,
    backoff: int = 1,
    max_delay: int = -1,
    max_jitter: int = 0,
    exceptions: Union[Exception, tuple[Exception]] = Exception,
):
    """Retry a function, later, in the background.

    Args:
        retry_interval (int): Time to wait in seconds between each retry. (Default: 5)
        max_retries (int): Maximum retries before giving up. (Default: 3)
        backoff (int): Multiplier to add between retry attempts. (Default: 1)
        max_delay (int): Maximum delay. (Default: -1, no limit)
        max_jitter (int): Maximum random jitter. (Default: 0, no jitter)
        exception (Exception): Exception or tuple of exceptions to retry. (Default: Exception Base class).
    """

    def decorator(func: Callable):
        async def wrapper(*args, **kwargs):
            retries = 0
            while retries < max_retries:
                try:
                    if inspect.iscoroutinefunction(func):
                        await asyncio.gather(func(*args, **kwargs))
                    else:
                        _ = func(*args, **kwargs)
                except exceptions as e:
                    retries += 1
                    if retries >= max_retries:
                        raise e
                    delay = retry_interval * (backoff**retries) + random.choice(range(0, max_jitter + 1))
                    if max_delay > 0:
                        delay = min(max_delay, delay)
                    logging.error(f"[retry later] Retrying in {delay}s due to {e}")
                    await asyncio.sleep(delay)

        def callback(*args, **kwargs):
            asyncio.run(wrapper(*args, **kwargs))

        def wrapper_threaded(*args, **kwargs):
            Thread(target=callback, args=args, kwargs=kwargs, daemon=True).start()

        return wrapper_threaded

    return decorator
