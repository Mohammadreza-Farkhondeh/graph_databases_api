from typing import Dict

from pydantic import BaseModel


class VertexCreate(BaseModel):
    class_name: str
    data: Dict


class VertexUpdate(BaseModel):
    rid: str
    data: Dict


class VertexDelete(BaseModel):
    rid: str
