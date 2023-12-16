from json import dumps
from typing import Any, Dict

from .base import QueryBuilder


class EdgeQueryBuilder(QueryBuilder):
    """
    concrete query builder for `orientdb Edges`
    implements abstract query builder
    methods will return queries for edge instances crud
    """

    def query_create(
            self, class_name: str, data: Dict[str, Any]
    ) -> str:
        """
        return query can be used for create an edge instance
        """
        query = f"CREATE EDGE {class_name} FROM {data.pop('from')} TO {data.pop('to')}"
        props = " ".join(f"{key}={value}" for key, value in data.items())
        if props:
            query += f"SET {props}"

        return query

    def query_update(self, instance_id: str, data: Dict[str, Any]) -> str:
        """
        return query for alter a record
        fields are case-sensitive
        {"Email": "a@b.com"}
        """
        raise Exception("error prone")
        # query = f"UPDATE {instance_id} MERGE {dumps(data)}"

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
            from_filter: str,
            to_filter: str,
            data: Dict[str, Any] = None,
    ) -> str:
        """
        return query for getting some edges based on conditions:
        input example:
          {"class_name": "Watched","from_filter": "(name = 'Luca')", "to_filter": "()", "direction": "<->", "data": {}}
        return example:
          MATCH {Class: Profiles, as: profile, where: (Name='Santo' AND Surname='OrientDB')
            }-HasFriend-{
          Class: Profiles, as: friend}
            RETURN $pathelements
            (https://orientdb.com/docs/last/gettingstarted/demodb/queries/DemoDB-Queries-Friendship.html)
        """
        query = f"MATCH {{Class:V, as:a, where:({from_filter})}}"
        query += f"-{class_name}-"
        query += f"{{Class:V, as:b, where:({to_filter})}}"

        if data:
            props = " AND ".join(f"{key}={value}" for key, value in data.items())
            query += props
        query += " RETURN $pathelements"

        return query
