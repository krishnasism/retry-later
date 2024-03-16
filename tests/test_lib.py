import time

import pytest

from retry_later import retry_later


@retry_later()
def write_to_file(file_name: str, body: str):
    with open(file_name, "w") as f:
        f.write(body)


@retry_later()
async def write_to_file_async(file_name: str, body: str):
    with open(file_name, "w") as f:
        f.write(body)


def test_success_once(temporary_file):
    write_to_file(temporary_file, "hello world")
    time.sleep(2)
    with open(temporary_file) as f:
        assert "hello world" in f.read()


@pytest.mark.asyncio
async def test_success_once_async(temporary_async_file):
    await write_to_file_async(temporary_async_file, "hello world")
    time.sleep(2)
    with open(temporary_async_file) as f:
        assert "hello world" in f.read()
