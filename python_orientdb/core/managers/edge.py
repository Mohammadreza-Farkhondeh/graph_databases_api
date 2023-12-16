from typing import Any, Dict

from pyorient.orient import OrientDB

from .base import Manager
from ..query_builders import EdgeQueryBuilder
from ..schema_validator import SchemaValidator


class EdgeManager(Manager):
    """
    concrete manager for `orientdb edges`
    implements abstract manager
    methods will execute command and queries on orientdb
    """

    def __init__(self, client: OrientDB):
        super().__init__(client)
        self.client = client
        self._query_builder = EdgeQueryBuilder()
        self._schema_validator = SchemaValidator(self.client)

    async def create(self, class_name: str, data: Dict[str, Any]) -> Dict:
        self._schema_validator.validate_class_properties(class_name, data)
        command = self._query_builder.query_create(class_name, data)
        result = self.client.command(command)
        return result[0].__dict__

    async def update(self, rid: str, data: Dict[str, Any]) -> Dict:
        query = self._query_builder.query_update(rid, data)
        i = self.client.command(query)
        result = self.client.record_load(rid)
        return result.__dict__

    async def delete(self, rid: str) -> Any:
        """
        WARNING! WARNING! WARNING!
        used orient.record_delete() and it destroyed the whole database,
        """
        command = self._query_builder.query_delete(rid)
        result = self.client.command(command)
        return result

    async def retrieve(
            self,
            class_name: str,
            out_filter: str = "1=1",
            in_filter: str = "1=1",
            data: Dict[str, Any] = None,
    ) -> Any:
        query = self._query_builder.query_retrieve(
            class_name, out_filter, in_filter, data
        )
        result = self.client.query(query)
        return result
