from typing import Dict

from pydantic import BaseModel


class EdgeCreate(BaseModel):
    class_name: str
    in_rid: str
    out_rid: str
    data: Dict


class EdgeUpdate(BaseModel):
    rid: str
    data: Dict


class EdgeDelete(BaseModel):
    rid: str
