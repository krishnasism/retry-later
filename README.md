# retry_later

`@retry_later` allows you to retry the execution of a function asynchronously in the background until it's done.

### Why?

For example, you can retry sending an email until it's sent.

## Installation

```bash
pip install retry-later
```

## Usage

Simply add `@retry_later` to your function. This also works with `async` functions.

```python
from my_very_python_real_email_client import send_mail_to_friend, send_text_to_friend

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
