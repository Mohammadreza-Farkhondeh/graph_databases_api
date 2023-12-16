from typing import List

from pydantic import BaseModel


class Vertex(BaseModel):
    vertexId: str
    attributes: dict = None


class UpsertVertices(BaseModel):
    vertexType: str
    vertices: List[Vertex]


class DeleteVertex(BaseModel):
    vertexType: str
    where: str = ""
