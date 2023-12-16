from typing import Tuple

from fastapi import Request
from httpx import AsyncClient

CLIENTS = {}


def get_user_db_credential(request: Request) -> Tuple:
    host = request.headers.get("X-orient-host")
    port = request.headers.get("X-orient-port")
    return host, port


async def set_client(request: Request) -> None:
    host, port = get_user_db_credential(request)
    client_id = f"{host}:{port}"

    if client_id not in CLIENTS:
        base_url = f"http://{host}:{port}/"
        CLIENTS[client_id] = AsyncClient(base_url=base_url)

    client = CLIENTS[client_id]
    request.state.orient = client
