from typing import Tuple
from fastapi import Request, HTTPException

from pyorient import OrientDB

from core import Orient

orient = Orient()
CLIENTS = {}


def get_user_db_credential(request: Request) -> Tuple:
    host = request.headers.get("X-orient-host")
    port = request.headers.get("X-orient-port")
    return host, port


def identify_user(request: Request) -> str:
    user_id = request.headers.get("X-user-id")
    return user_id


async def set_client(request: Request):
    user_id = identify_user(request)

    if user_id not in CLIENTS:
        host, port = get_user_db_credential(request)
        CLIENTS[user_id] = OrientDB(host=host, port=port)

    orient.client = CLIENTS[user_id]
    request.state.orient = orient
