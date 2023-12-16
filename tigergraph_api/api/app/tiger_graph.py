import random
from typing import Union, Dict

from pyTigerGraph import TigerGraphConnection

letters = "abcdefghijklmnopqrstuvwxyz"


class TigerGraph:
    connections: Dict = {}
    conn: Union[TigerGraphConnection, None] = None
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def add_client(self, host: str, graphname: str, username: str, password: str, secret: str = None) -> str:
        conn = TigerGraphConnection(host=host, graphname=graphname, username=username, password=password)
        secret = secret if secret else conn.createSecret()
        conn.getToken(secret)

        conn_id = ''.join(random.choice(letters) for i in range(10))
        self.connections[conn_id] = conn
        return conn_id


tg = TigerGraph()
tg.conn = TigerGraphConnection() if not tg.conn else tg.conn
