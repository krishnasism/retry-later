import asyncio
import random

import requests

from retry_later import retry_later

# Should return 404
doesnt_exist_url: str = "https://spacehook-4-o4569495.deta.app/api/hook/doesnt-exist"
# Should return 200
exists_url: str = "https://spacehook-4-o4569495.deta.app/api/hook/ok"

loop = asyncio.new_event_loop()


@retry_later(exceptions=ConnectionError, max_retries=10)
async def call_hook_from_choice(url_choices: tuple[str]):
    response = requests.get(random.choice(url_choices))
    if response.status_code == 404:
        raise ConnectionError(f"Could not connect. Response: {response.status_code}")
    else:
        print("Called endpoint successfully!")


asyncio.set_event_loop(loop)

# Randomize pass/fail to test
url_choices_tuple = (doesnt_exist_url, exists_url)
asyncio.run(call_hook_from_choice(url_choices_tuple))

print("I am here.. waiting for you to run")
print(1 + 1)

# Simulate a long running application, can also use loop.run_forver() to test
asyncio.run(asyncio.sleep(100))
exit(1)
