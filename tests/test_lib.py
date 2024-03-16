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


def test_success_once():
    write_to_file("test.txt", "hello world")
    time.sleep(2)
    with open("test.txt") as f:
        assert "hello world" in f.readlines()


@pytest.mark.asyncio
async def test_success_once_async():
    await write_to_file_async("test1.txt", "hello world")
    time.sleep(2)
    with open("test1.txt") as f:
        assert "hello world" in f.readlines()
