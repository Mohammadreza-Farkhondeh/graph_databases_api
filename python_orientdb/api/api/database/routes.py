try:
    from typing import Annotated
except ImportError:
    from typing_extensions import Annotated

from fastapi import APIRouter, HTTPException, responses
from api.api.middlewares import orient
from .schemas import ConnectHost, ConnectDatabase


router = APIRouter()


@router.post('/all')
def connect_host(data: ConnectHost):
    """
    send host, port, user and password to connect the host have orient
    response will be list of databases
    """
    orient.connect_to_orient(data.user, data.password)
    database_list = orient.list_databases()
    return database_list


@router.post('/')
def connect_database(data: ConnectDatabase):
    """
    send host, port, user, password and database name to connect to database
    response ok
    """
    orient.open_database(data.database, data.user, data.password)
    result = orient.get_schema()
    return result
