try:
    from typing import Annotated
except ImportError:
    from typing_extensions import Annotated

from fastapi import APIRouter, HTTPException, responses
from api.api.middlewares import orient
from .schemas import ClassCreate, ClassUpdate

router = APIRouter()


@router.post("/")
async def create_class(class_data: ClassCreate):
    """
    send a class name then it will be created in the database
    optional:
        - extends: select the class will extend, default is `V`
        - abstract: boolean, default False
    """
    result = await orient.class_manager.create(
        class_data.class_name,
        class_data.extends,
        class_data.abstract,
    )
    response = {"detail": f"class {class_data.class_name}", "method": "create", "result": result}
    return responses.JSONResponse(status_code=201, content=response)


@router.put("/")
async def update_class(class_data: ClassUpdate):
    """
    class properties will be updated:
        - create a property: by name
        - alter a property: by name, attribute, value
    """
    result = await orient.class_manager.update(
        class_data.class_name, class_data.properties
    )
    response = {"detail": f"class {class_data.class_name}", "method": "update", "result": result}
    return responses.JSONResponse(status_code=200, content=response)


@router.delete("/")
async def delete_class():
    """
    classes cant be deleted
    """
    raise HTTPException(status_code=403, detail="Classes can't be deleted temporarily.")


@router.get("/")
async def get_class(class_name: str):
    """
    should get a class name in query parameters
    response include the class details
    """
    try:
        result = await orient.class_manager.retrieve(class_name)
    except ValueError as e:
        raise HTTPException(status_code=404)

    response = {"detail": f"class {class_name}", "method": "retrieve", "result": result}
    return responses.JSONResponse(status_code=200, content=response)


@router.get("/all")
async def get_all_classes():
    """
    response will be all classes in database details
    """
    result = await orient.class_manager.retrieve()
    response = {"detail": "all database classes", "method": "retrieve", "result": result}
    return responses.JSONResponse(status_code=200, content=response)
