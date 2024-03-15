import asyncio
import inspect
import logging
from threading import Thread


def retry_later(
    retry_interval: int = 5,
    max_retries: int = 3,
    exception: Exception = Exception,
    # more args to be added soon
):
    """Retry a function, later, in the background.

    Args:
        retry_interval (int): Time to wait between each retry (in seconds). Default: 5..
        max_retries (int): Maximum retries before giving up. Default: 3.
        exception (Exception): Exception to catch to retry. Default: Any Exception.
    """

    def decorator(func: callable):
        async def wrapper(*args, **kwargs):
            retries = 0
            while retries < max_retries:
                try:
                    if inspect.iscoroutinefunction(func):
                        await asyncio.gather(func(*args, **kwargs))
                    else:
                        _ = func(*args, **kwargs)
                except exception as e:
                    retries += 1
                    if retries >= max_retries:
                        raise e from exception
                    logging.error(
                        f"[retry later] Retrying in {retry_interval}s due to {e}"
                    )
                    await asyncio.sleep(retry_interval)

        def callback(*args, **kwargs):
            asyncio.run(wrapper(*args, **kwargs))

        def wrapper_threaded(*args, **kwargs):
            t = Thread(target=callback, args=args, kwargs=kwargs)
            t.daemon = True
            t.start()

        return wrapper_threaded

    return decorator
