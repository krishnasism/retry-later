import random

import requests
from fastapi import APIRouter, status
from fastapi.responses import PlainTextResponse, Response

from retry_later import retry_later

routers = APIRouter()


@routers.get(
    "/health",
    response_model=str,
    description="health check",
    name="health",
    response_class=PlainTextResponse,
)
async def health() -> Response:
    doesnt_exist_url: str = "https://spacehook-4-o4569495.deta.app/api/hook/doesnt-exist"
    exists_url: str = "https://spacehook-4-o4569495.deta.app/api/hook/ok"
    url_choices_tuple = (doesnt_exist_url, exists_url)
    await call_hook_from_choice(url_choices_tuple)
    return Response(
        content="OK",
        status_code=status.HTTP_200_OK,
        headers={"content-Type": "text/plain"},
    )


@retry_later(exceptions=ConnectionError, max_retries=10)
async def call_hook_from_choice(url_choices: tuple[str]):
    response = requests.get(random.choice(url_choices))
    if response.status_code == 404:
        raise ConnectionError(f"Could not connect. Response: {response.status_code}")
    else:
        print("Called endpoint successfully!")


"""Console Logs:

INFO:     127.0.0.1:56600 - "GET /api/v1/health HTTP/1.1" 200 OK
ERROR:root:[retry later] Retrying in 5s due to Could not connect. Response: 404
ERROR:root:[retry later] Retrying in 5s due to Could not connect. Response: 404
Called endpoint successfully!

"""

"""
You can see that the retry happens after the /health endpoint response is sent.
It doesn't wait for call_hook_from_choice to execute.
"""
