import time

from retry_later import retry_later


@retry_later()
def write_to_file(file_name: str, body: str):
    with open(file_name, "w") as f:
        f.write(body)


def test_success_once():
    write_to_file("test.txt", "hello world")
    time.sleep(5)
    with open("test.txt") as f:
        assert "hello world" in f.readlines()
