import asyncio

from retry_later import retry_later
import time

loop = asyncio.get_event_loop()


@retry_later(retry_interval=5, max_retries=3)
async def my_function():
    print("Running my_function")
    time.sleep(5)
    raise Exception("Function failed")


async def main():
    my_function()
    print("Hello")


asyncio.run(main())
loop.run_forever()
