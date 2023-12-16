from typing import List, Dict, Union

import pyorient.exceptions
from pyorient.orient import OrientDB
from httpx import AsyncClient

from .base import Manager
from ..query_builders import ClassQueryBuilder


class ClassManager(Manager):
    """
    concrete binary manager for `orientdb classes`
    implements abstract manager
    methods will execute command and queries on orientdb using orient binary protocol
    """

    def __init__(self, client: OrientDB):
        self.client = client
        self._query_builder = ClassQueryBuilder()

    async def create(
            self,
            class_name: str,
            extends: Union[str, None] = None,
            abstract: bool = False,
    ) -> bool:
        """
        return class id if database didn't exist, otherwise ValueError
        """
        query = self._query_builder.query_create(class_name, extends, abstract)
        try:
            result = self.client.command(query)
            return True
        except pyorient.exceptions.PyOrientSchemaException as e:
            if "already exists in current database" in e:
                raise ValueError("database already exists")

    async def update(self, class_name: str, data: Dict[str, List]) -> bool:
        commands: List = self._query_builder.query_update(class_name, data)
        (self.client.command(command) for command in commands)
        return True

    async def delete(self, instance_id: str) -> Exception:
        raise Exception("Classes cant be deleted temporary.")

    async def retrieve(self, class_name: Union[str, None] = None) -> List[Dict]:
        query = self._query_builder.query_retrieve(class_name)
        res = self.client.query(query)
        if not res:
            raise Exception("nothing found!")
        result = [r.__dict__ for r in res]
        return result
