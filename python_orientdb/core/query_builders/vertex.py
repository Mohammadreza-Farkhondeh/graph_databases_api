from json import dumps
from typing import Any, Dict

from .base import QueryBuilder


class VertexQueryBuilder(QueryBuilder):
    """
    concrete query builder for `orientdb Vertices`
    implements abstract query builder
    methods will return queries for vertex instances crud
    """

    def query_create(self, class_name: str, data: Dict[str, Any]) -> str:
        """
        return query can be used for create a vertex instance
        """
        query = f"CREATE VERTEX {class_name}"
        props = " ".join(f"{key}={value}" for key, value in data.items())
        if props:
            query += f"SET {props}"

        return query

    def query_update(self, instance_id: str, data: Dict[str, Any]) -> str:
        """
        return query for alter a class
        example data input :
                ([{"property":"Age", "attribute":"MANDATORY"}, "value":"true"])
        """
        raise Exception("error prone")
        query = f"UPDATE {instance_id} MERGE {dumps(data)}"

        return query

    def query_delete(self, instance_id: str) -> str:
        """
        return instance delete query by its id
        """
        query = f"DELETE {instance_id}"
        return query

    def query_retrieve(
            self,
            class_name: str,
            vertex_filter: str,
    ) -> str:
        # query = f"SELECT FROM {class_name} "
        # query += filter

        query = "MATCH {class:%s, as:c, where:(%s)} RETURN $pathelements" % (class_name, vertex_filter,)

        return query
