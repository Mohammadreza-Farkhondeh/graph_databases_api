try:
    from typing import Annotated
except ImportError:
    from typing_extensions import Annotated
from fastapi import APIRouter, Depends, responses

from api.api.middlewares import orient
from core import Orient
from .schemas import EdgeCreate, EdgeUpdate, EdgeDelete

router = APIRouter()


@router.post("/")
async def create_edge(edge_data: EdgeCreate):
    """
    send two vertex rid and edge class name to create relationship
    data is optional (not for mandatory properties)
    """
    data = edge_data.__dict__
    data["in"] = data.pop("in_rid")
    data["out"] = data.pop("our_rid")
    result = await orient.edge_manager.create(edge_data.class_name, data)
    response = {"detail": f"{edge_data.class_name} edge from{data['out']} to {data['in']}",
                "method": "create", "result": result}
    return responses.JSONResponse(status_code=201, content=response)


@router.put("/")
async def update_edge(edge_data: EdgeUpdate):
    """
    send rid and data to update the record
    """
    result = await orient.edge_manager.update(edge_data.rid, edge_data.data)
    response = {"detail": f"edge {edge_data.rid}", "method": "update", "result": result}
    return responses.JSONResponse(status_code=200, content=response)


@router.delete("/")
async def delete_edge(edge_data: EdgeDelete):
    """
    send rid to delete record
    """
    result = await orient.edge_manager.delete(edge_data.rid)
    response = {"detail": f"edge {edge_data.rid}", "method": "delete", "result": result}
    return responses.JSONResponse(status_code=204, content=response)


@router.get("/")
async def get_edge(class_name: str, in_filter: str = "", out_filter: str = "", data: dict = None):
    """
    will query in MATCH, edge class name is mandatory, else optional
    """
    result = await orient.edge_manager.retrieve(class_name, out_filter, in_filter, data)
    response = {"detail": "retrieve edges", "method": "delete", "result": result}
    return responses.JSONResponse(status_code=200, content=response)
