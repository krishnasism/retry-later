import os

import pytest


@pytest.fixture
def temporary_file():
    file_name = "test.txt"
    yield file_name
    os.remove(file_name)


@pytest.fixture
def temporary_async_file():
    file_name = "test_async.txt"
    yield file_name
    os.remove(file_name)
