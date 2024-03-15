# retry_later

`@retry_later` allows you to execute a function asynchronously in the background and automatically retry it if an exception occurs, up to a specified maximum number of retries.

Why?

For example, you can retry sending an email until it's actually sent.

## Installation

For now `git clone` or copy the `retry_later` folder. Will be working on it more.

## Usage

Simply add `@retry_later` to your function.

```python
import logging

# Import the decorator
from retry_later import retry_later
from my_very_python_real_email_client import send_mail_to_friend

@retry_later(retry_interval=10, max_retries=5, exception=ConnectionError)
def send_email(param1, param2):
    send_mail_to_friend(email="veryrealperson@veryrealemail.haha", body="hi!")

my_function(param1, param2)
