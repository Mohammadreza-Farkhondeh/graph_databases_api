import pytest

from core.managers import ClassManager, EdgeManager, VertexManager


# TODO use params decorator to test different queries
# TODO manager declarations can be in some fixtures


@pytest.mark.asyncio  # to tell pytest methods under test are async
class TestClassManager:
    async def test_create(self, mock_orient_client):
        cm = ClassManager(mock_orient_client)
        class_name = "Foo"
        result = await cm.create(class_name, "V", True)

        assert result == True
        mock_orient_client.command.assert_called_with(f"CREATE CLASS {class_name} EXTENDS V ABSTRACT")

    async def test_update(self, mock_orient_client):
        cm = ClassManager(mock_orient_client)
        class_name = "Foo"
        result = await cm.update(class_name,
                                 data={"update": [{"property": "Name", "attribute": "MANDATORY", "value": "true"}],
                                       "create": [{"property": "Age", "type": "INTEGER"}]})
        assert result == True
        mock_orient_client.command.assert_called_with(
            f"CREATE PROPERTY {class_name}.Age INTEGER; ALTER PROPERTY {class_name}.Name MANDATORY true")

    async def test_delete(self, mock_orient_client):
        cm = ClassManager(mock_orient_client)
        with pytest.raises(Exception) as excinfo:
            await cm.delete("Foo")
        assert str(excinfo.value) == "Classes cant be deleted temporary."

    async def test_retrieve(self, mocker, mock_orient_client):
        cm = ClassManager(mock_orient_client)
        mock_record = mocker.Mock()
        class_name = "Foo"
        mock_record.__dict__ = {"name": class_name,
                                "properties": [{"name": "name", "type": "STRING"}, {"name": "age", "type": "INTEGER"}]}
        mock_orient_client.query.return_value = [mock_record, 1, 2]
        result = await cm.retrieve(class_name)
        assert result == {"name": class_name,
                          "properties": [{"name": "name", "type": "STRING"}, {"name": "age", "type": "INTEGER"}]}
        mock_orient_client.query.assert_called_with(
            f"SELECT * FROM (SELECT expand(classes) FROM metadata:schema) WHERE name='{class_name}'")


@pytest.mark.asyncio
class TestEdgeManager:
    async def test_create(self, mock_orient_client):
        em = EdgeManager(mock_orient_client)
        result = await em.create("Foo", {"in": "#11:0", "out": "#11:1"})
        assert result == True
        mock_orient_client.record_delete.assert_called_with(-1, {"@Foo": {"in": "#11:0", "out": "#11:1"}})

    async def test_update(self, mock_orient_client):
        em = EdgeManager(mock_orient_client)
        result = await em.update("#12:0", data={"name": "new_test"})
        assert result == {'_OrientRecord__o_class': None,
                          '_OrientRecord__o_storage': {},
                          '_OrientRecord__rid': '#12:0',
                          '_OrientRecord__version': None}

        mock_orient_client.command.assert_called_with('UPDATE #12:0 MERGE {"name": "new_test"}')

    async def test_delete(self, mock_orient_client):
        em = EdgeManager(mock_orient_client)
        result = await em.delete("#12:0")
        assert result == True
        mock_orient_client.record_delete.assert_called_with(12, 0)

    async def test_retrieve(self, mock_orient_client):
        em = EdgeManager(mock_orient_client)
        result = await em.retrieve("Foo", "(Name = 'John')", "(Name = 'Jane')")
        assert result == [{"key": "value"}, {"key": "value"}]
        mock_orient_client.query.assert_called_with(
            "MATCH {Class:V, as:a, where:((Name = 'John'))}-Foo-{Class:V, as:b, where:((Name = 'Jane'))} RETURN $pathelements")


@pytest.mark.asyncio
class TestVertexManager:
    async def test_create(self, mock_orient_client):
        em = ClassManager(mock_orient_client)
        result = await em.create("Foo", {})
        assert result == True
        mock_orient_client.record_delete.assert_called_with(-1, {"@Foo": {}})

    async def test_update(self, mock_orient_client):
        em = VertexManager(mock_orient_client)
        result = await em.update("#12:0", data={"name": "new_test"})
        assert result == {'_OrientRecord__o_class': None,
                          '_OrientRecord__o_storage': {},
                          '_OrientRecord__rid': '#12:0',
                          '_OrientRecord__version': None}

        mock_orient_client.command.assert_called_with('UPDATE #12:0 MERGE {"name": "new_test"}')

    async def test_delete(self, mock_orient_client):
        em = VertexManager(mock_orient_client)
        result = await em.delete("#12:0")
        assert result == True
        mock_orient_client.record_delete.assert_called_with(12, 0)

    async def test_retrieve(self, mock_orient_client):
        em = VertexManager(mock_orient_client)
        result = await em.retrieve("Foo", "(Name = 'John')")
        assert result == [{"key": "value"}, {"key": "value"}]
        mock_orient_client.query.assert_called_with(
            "MATCH {class:Foo, as:c, where:((Name = 'John'))} RETURN $pathelements")
