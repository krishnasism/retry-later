import os
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


@retry_later(retry_interval=5)
def write_to_only_new_file(file_name: str, message: str):
    with open(file_name, "x") as f:
        f.write(message)


@retry_later(retry_interval=5)
async def write_to_only_new_file_async(file_name: str, message: str):
    with open(file_name, "x") as f:
        f.write(message)


@retry_later()
async def read_from_file_async(file_name: str, body: str):
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


def test_success_after_exception(duplicate_file):
    with open(duplicate_file, "w") as f:
        f.write("this is not visible")

    # First time should fail due to file already existing
    write_to_only_new_file(duplicate_file, "this is visible")

    os.remove(duplicate_file)
    time.sleep(6)
    with open(duplicate_file) as f:
        lines = f.readlines()
        assert "this is visible" in lines
        assert "this is not visible" not in lines


@pytest.mark.asyncio
async def test_success_after_exception_async(duplicate_file_async):
    with open(duplicate_file_async, "w") as f:
        f.write("this is not visible")

    # First time should fail due to file already existing
    await write_to_only_new_file_async(duplicate_file_async, "this is visible")

    os.remove(duplicate_file_async)
    time.sleep(6)
    with open(duplicate_file_async) as f:
        lines = f.readlines()
        assert "this is visible" in lines
        assert "this is not visible" not in lines
