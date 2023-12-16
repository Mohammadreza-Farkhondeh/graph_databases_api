from typing import Union, Any, List
import pyorient as pyorient

from .managers import ClassManager, EdgeManager, VertexManager


class Orient:
    def __init__(self):
        self.client: Union[pyorient.OrientDB, None] = None

    # Singleton
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @property
    def class_manager(self):
        if not self.client:
            raise AttributeError("Orient.client should not be None")
        return ClassManager(self.client)

    @property
    def edge_manager(self):
        if not self.client:
            raise AttributeError("Orient.client should not be None")
        return EdgeManager(self.client)

    @property
    def vertex_manager(self):
        if not self.client:
            raise AttributeError("Orient.client should not be None")
        return VertexManager(self.client)

    def connect_to_orient(self, user: str, password: str):
        if not self.client:
            raise AttributeError("Orient.client should not be None")
        self.client.connect(user, password)

    def list_databases(self) -> List:
        if not self.client:
            raise AttributeError("Orient.client should not be None")
        result = self.client.query("LIST DATABASES")
        return result

    def open_database(self, db_name: str, user: str, password: str):
        if not self.client:
            raise AttributeError("Orient.client should not be None")
        self.client.db_open(db_name, user, password)

    def get_schema(self, db_name: str):
        if not self.client:
            raise AttributeError("Orient.client should not be None")
        result = self.client.query("select * from metadata:schema")
        return result

    def close(self):
        if not self.client:
            raise AttributeError("Orient.client should not be None")
        self.client.db_close()
        self.client.close()
