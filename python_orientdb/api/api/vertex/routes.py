try:
    from typing import Annotated
except ImportError:
    from typing_extensions import Annotated

from fastapi import APIRouter, Depends, responses

from api.api.middlewares import orient
from core import Orient
from .schemas import VertexCreate, VertexUpdate, VertexDelete

router = APIRouter()


@router.post("/")
async def create_vertex(vertex_data: VertexCreate):
    """
    like class name, data is mandatory here
    """
    result = await orient.vertex_manager.create(vertex_data.class_name, vertex_data.data)
    response = {"detail": f"{vertex_data.class_name} vertex", "method": "create", "result": result}
    return responses.JSONResponse(status_code=201, content=response)


@router.put("/")
async def update_vertex(vertex_data: VertexUpdate):
    """
    update vertex by rid with data
    """
    result = await orient.vertex_manager.update(vertex_data.rid, vertex_data.data)
    response = {"detail": f"vertex {vertex_data.rid}", "method": "update", "result": result}
    return responses.JSONResponse(status_code=200, content=response)


@router.delete("/")
async def delete_vertex(vertex_data: VertexDelete):
    """
    delete vertex by rid
    """
    result = await orient.vertex_manager.delete(vertex_data.rid)
    response = {"detail": f"vertex {vertex_data.rid}", "method": "delete", "result": result}
    return responses.JSONResponse(status_code=204, content=response)


@router.get("/")
async def get_vertex(class_name: str, vertex_filter: str = ""):
    """
    query MATCH by class name, can have filter
    """
    result = await orient.vertex_manager.retrieve(class_name, vertex_filter)
    return result
