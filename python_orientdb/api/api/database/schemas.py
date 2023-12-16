from pydantic import BaseModel


class ConnectHost(BaseModel):
    host: str
    port: int
    user: str
    password: str


class ConnectDatabase(ConnectHost):
    database: str
