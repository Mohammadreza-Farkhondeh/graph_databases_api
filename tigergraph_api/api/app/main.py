from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware

from api.app.routes import edge_router, vertex_router, graph_router
from api.app.tiger_graph import tg

app = FastAPI()
app.description = "all routes should have X-conn-id in header, if you dont have one, reach /connect to get id"


app.add_middleware(
    CORSMiddleware,
    allow_origins=["localhost:3000", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# @app.middleware("http")
# async def check_conn_id_middleware(request: Request, call_next):
#     if request.url.path.startswith("/api/"):
#         if request.url.path.startswith("/api/graph/connect"):
#             pass
#         else:
#             if "X-conn-id" not in request.headers:
#                 return Response("X-conn-id should be in header", 400)
#             conn_id = request.headers["X-conn-id"]
#             try:
#                 tg.conn = tg.connections[conn_id]
#             except KeyError:
#                 return Response("Please connect First, see /connect", 400)
#     response = await call_next(request)
#     return response


app.include_router(edge_router, prefix="/api/edges", tags=["edges"])
app.include_router(vertex_router, prefix="/api/vertices", tags=["vertices"])
app.include_router(graph_router, prefix="/api/graph", tags=["graphs"])
