try:
    from typing import Annotated
except ImportError:
    from typing_extensions import Annotated

from fastapi import Request, Depends, HTTPException
from pyTigerGraph import TigerGraphConnection

connections = {}


async def tg_dependency(request: Request):
    try:
        host = request.headers["X-host"]
        graph_name = request.headers["X-graph-name"]
    except KeyError:
        host = "http://127.0.0.1"
        graph_name = "MyGraph"

    key = f"{host}/{graph_name}"
    if key in connections:
        return connections[key]
    else:
        raise HTTPException(400, "please reach /connect first")


class TigerGraph:
    def __init__(self):
        self.connections = {}


TG_dep = Annotated[TigerGraphConnection, Depends(tg_dependency)]
fmt = "py"
