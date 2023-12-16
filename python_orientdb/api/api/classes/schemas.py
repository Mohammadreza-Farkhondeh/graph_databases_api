from typing import Union, Dict

from pydantic import BaseModel


class ClassCreate(BaseModel):
    class_name: str
    extends: Union[str, None] = None
    abstract: bool = False


class ClassUpdate(BaseModel):
    class_name: str
    properties: Dict
