[![latest](https://github.com/krishnasism/retry-later/actions/workflows/publish.yml/badge.svg)](https://github.com/krishnasism/retry-later/actions/workflows/publish.yml)
[![tests](https://github.com/krishnasism/retry-later/actions/workflows/test.yml/badge.svg?branch=main)](https://github.com/krishnasism/retry-later/actions/workflows/test.yml)
[![Coverage Status](https://coveralls.io/repos/github/krishnasism/retry-later/badge.svg?branch=main)](https://coveralls.io/github/krishnasism/retry-later?branch=main)
# retry_later

`@retry_later` allows you to retry the execution of a function asynchronously in the background until it's done.

### Why?

For example, you can retry sending an email until it's sent.

## Installation

```bash
pip install retry-later
```

## Usage

Simply add `@retry_later()` to your function. This also works with `async` functions.

Look inside the `examples` folder for more examples!

Here's a simple demonstration:

```python
from my_very_python_real_email_client import send_mail_to_friend, send_text_to_friend
import asyncio

# Create new event loop
loop = asyncio.new_event_loop()

# Import the decorator
from retry_later import retry_later

@retry_later(retry_interval=10, max_retries=5, exception=ConnectionError)
def send_email():
    send_mail_to_friend(email="veryrealperson@veryrealemail.haha", body="hi!")

@retry_later(retry_interval=10, max_retries=5, exception=ConnectionError)
async def send_a_text():
    await send_text_to_friend(number="+123456789", body="hi! texting you")

send_email()
asyncio.run(send_a_text())

# Other stuff
print("Hi - I am here!! I complete before my_function!")

# event loop must be running for retry_later to work
loop.run_forever()
