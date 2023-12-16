from fastapi import FastAPI, Request

from api.api.middlewares import set_client
from api.api.database.routes import router as database_routes
from api.api.classes.routes import router as class_routes
from api.api.edge.routes import router as edge_routes
from api.api.vertex.routes import router as vertex_routes

app = FastAPI(title="OrientDB API")

app.include_router(database_routes, prefix="/database", tags=["databases"])
app.include_router(class_routes, prefix="/class", tags=["classes"])
app.include_router(edge_routes, prefix="/edge", tags=["edges"])
app.include_router(vertex_routes, prefix="/vertex", tags=["vertices"])


@app.middleware("http")
async def orient_middle_ware(request: Request, call_next):
    await set_client(request)
    response = await call_next(request)
    return response
