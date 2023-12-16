from typing import List

from pydantic import BaseModel


class Edge(BaseModel):
    sourceVertexType: str
    sourceVertexId: str
    edgeType: str
    targetVertexType: str
    targetVertexId: str
    attributes: dict = None


class UpsertEdges(BaseModel):
    edgeType: str
    edges: List[Edge]


class DeleteEdge(BaseModel):
    sourceVertexType: str
    sourceVertexId: str
    edgeType: str = ""
    targetVertexType: str = ""
    targetVertexId: str = ""
    where: str = ""
