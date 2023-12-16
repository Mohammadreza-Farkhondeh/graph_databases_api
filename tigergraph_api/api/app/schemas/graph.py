from typing import Union

from pydantic import BaseModel


class UpsertJob(BaseModel):
    data: Union[str, object]
    atomic: bool = False
    newVertexOnly: bool = False
    vertexMustExist: bool = False
    updateVertexOnly: bool = False


class Connect(BaseModel):
    host: str
    graphname: str
    username: str
    password: str
    secret: str = None
