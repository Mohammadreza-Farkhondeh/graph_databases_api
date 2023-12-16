from typing import Dict, List, Union, Any

from .base import QueryBuilder


class ClassQueryBuilder(QueryBuilder):
    """
    concrete query builder for `orientdb classes`
    implements abstract query builder
    methods will return queries for class crud (not instances, but classes)
    """

    def query_create(
            self,
            class_name: str,
            extends: Union[None, str] = "V",
            abstract: bool = False,
    ) -> str:
        """
        return query creates a class that can be abstract or extend other class
        """
        query = f"CREATE CLASS {class_name} "
        if extends:
            query += f"EXTENDS {extends} "
        if abstract:
            query += "ABSTRACT"
        return query

    def query_update(self, class_name: str, data: Dict[str, List]) -> List[str]:
        """
        return query for alter a class
        example data input :
                ({"update": [{"property":"Age", "attribute":"MANDATORY", "value":"true"}, ...],
                  "create": [{"property": "birth", "type": "STRING"}, ...]})
        """
        commands = []
        if "create" in data:
            # [reference](https://orientdb.com/docs/last/general/Types.html)
            types = ("BOOLEAN", "INTEGER", "FLOAT", "DATETIME", "STRING")
            if not all(i['type'] in types for i in data['create']):
                raise ValueError("types not supported")

            try:
                commands + [
                    f"CREATE PROPERTY {class_name}.{prop['property']} {prop['type']}"
                    for prop in data["create"]
                ]
            except KeyError as e:
                raise KeyError('create should implement {"property": "name", "type": "STRING"}')

        if "update" in data:
            try:
                commands + [
                    f"ALTER PROPERTY {class_name}.{prop['property']} {prop['attribute']} {prop['value']}"
                    for prop in data["update"]
                ]
            except KeyError:
                raise KeyError('update should implement {"property": "name", "attribute": "MANDATORY", "value": "true"}')
        return commands

    def query_delete(self, class_name: str) -> Exception:
        """
        classes cant be delete NOW
        """
        raise Exception("Classes cant be deleted temporary.")

    def query_retrieve(self, class_name: Union[str, None] = None) -> str:
        query = "SELECT classes FROM metadata:schema"
        if class_name:
            query = f"SELECT * FROM (SELECT expand(classes) FROM metadata:schema) WHERE name='{class_name}'"

        return query
