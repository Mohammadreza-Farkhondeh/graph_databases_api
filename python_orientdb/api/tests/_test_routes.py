from fastapi.testclient import TestClient

from api.api.classes.schemas import ClassCreate, ClassUpdate
from api.api.edge.schemas import EdgeCreate, EdgeUpdate, EdgeDelete
from api.api.vertex.schemas import VertexCreate, VertexDelete
from api.app import app

client = TestClient(app)


class TestClassRoutes:
    def test_create_class(self):
        class_data = ClassCreate(
            class_name="Test",
            properties={"name": "STRING", "age": "INTEGER"},
            extends="V",
            abstract=False,
        )
        response = client.post("/class/", json=class_data.dict())
        assert response.status_code == 200
        assert response.json() == {
            "class_name": "Test",
            "method": "create",
            "result": True,
        }

    def test_update_class(self):
        class_data = ClassUpdate(
            class_name="Test",
            properties={"name": "STRING", "age": "INTEGER"},
        )
        response = client.put("/class/", json=class_data.dict())
        assert response.status_code == 200
        assert response.json() == {
            "class_name": "Test",
            "method": "update",
            "result": True,
        }

    def test_delete_class(self):
        response = client.delete("/class/")
        assert response.status_code == 400
        assert response.json() == {"detail": "Classes can't be deleted temporarily."}

    def test_get_class(self):
        response = client.get("/class/", params={"class_name": "Test"})
        assert response.status_code == 200
        assert response.json() == {
            "name": "Test",
            "defaultClusterId": 12,
            "clusterIds": [12],
            "clusterSelection": "round-robin",
            "overSize": 0.0,
            "strictMode": False,
            "abstract": False,
            "properties": [
                {"name": "name", "type": 7},
                {"name": "age", "type": 1},
            ],
            "superClass": "V",
            "superClasses": ["V"],
            "customFields": {},
            "indexes": [],
        }

    def test_get_all_classes(self):
        response = client.get("/class/all")
        assert response.status_code == 200


class TestEdgeRoutes:
    def test_create_edge(self):
        edge_data = EdgeCreate(
            class_name="Friend",
            in_rid="#12:0",
            out_rid="#13:0",
            data={"since": "2020-01-01"},
        )
        response = client.post("/edge/", json=edge_data.dict())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "class_name": "Friend",
            "in_rid": "#12:0",
            "out_rid": "#13:0",
            "data": {"since": "2020-01-01"},
        })

    def test_update_edge(self):
        edge_data = EdgeUpdate(
            rid="#10:0",
            data={"since": "2021-01-01"},
        )
        response = client.put("/edge/", json=edge_data.dict())
        assert response.status_code == 200
        assert response.json() == {
            "rid": "#10:0",
            "data": {"since": "2021-01-01"},
        }

    def test_delete_edge(self):
        edge_data = EdgeDelete(
            rid="#10:0",
        )
        response = client.delete("/edge/", json=edge_data.dict())
        assert response.status_code == 200
        assert response.json() == {
            "rid": "#10:0",
            "method": "delete",
            "result": True,
        }

    def test_get_edge(self):
        response = client.get("/edge/", params={"class_name": "Friend", "data": {"since": "2020-01-01"}})
        assert response.status_code == 200
        assert response.json() == {
            "edges": [
                {
                    "class_name": "Friend",
                    "in_rid": "#12:0",
                    "out_rid": "#13:0",
                    "data": {"since": "2020-01-01"}}
            ]
        }


class TestVertexRoutes:
    def test_create_vertex(self):
        vertex_data = VertexCreate(
            class_name="Person",
            data={"name": "Alice", "age": 25},
        )
        response = client.post("/vertex/", json=vertex_data.dict())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "class_name": "Person",
            "data": {"name": "Alice", "age": 25},
        })

    def test_delete_vertex(self):
        vertex_data = VertexDelete(
            rid="#14:0",
        )
        response = client.delete("/vertex/", json=vertex_data.dict())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "rid": "#14:0",
            "method": "delete",
            "result": True,
        })

    def test_get_vertex(self):
        response = client.get("/vertex/", params={"class_name": "Person", "data": {"name": "Alice"}})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "vertices": [
                {
                    "class_name": "Person",
                    "data": {"name": "Alice", "age": 25},
                }]})