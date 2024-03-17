import asyncio
import time

from retry_later import retry_later

loop = asyncio.new_event_loop()


@retry_later(retry_interval=5, max_retries=3, backoff=2)
def my_function():
    print("Running my_function")
    time.sleep(5)
    raise Exception("Function failed")


def main():
    my_function()
    print("Hello")


main()

print("Hi - I am here!! I complete before my_function!")

loop.run_forever()
