from typing import Any

from pyorient.exceptions import PyOrientSchemaException
from pyorient.orient import OrientDB


class SchemaValidator:
    def __init__(self, client: OrientDB):
        self.client = client

    def get_schema(self, class_name: str) -> dict:
        classes = self.client.query("SELECT FROM metadata:schema")[0]['classes']
        return classes[class_name]

    def validate_class_properties(
            self, class_name: str, properties: dict[str, Any]
    ) -> None:
        class_schema = self.get_schema(class_name)

        # Checking for non exist keys
        for key, prop in properties.items():
            if not any(p["name"] == prop["name"] for p in class_schema["properties"]):
                raise PyOrientSchemaException(
                    f"property '{prop['name']}' is not defined for class '{class_name}'.",
                    [],
                )

        # Checking for existence of mandatory keys
        for prop in class_schema["properties"]:
            if prop["mandatory"] and prop["name"] not in properties:
                raise PyOrientSchemaException(
                    f"Mandatory property '{prop['name']}' is missing in create data for class '{class_name}'.",
                    [],
                )
