import pytest
from pyorient import OrientDB
from pyorient.otypes import OrientRecord

from core.orient import Orient


# TODO change returns to yield to safe teardown


@pytest.fixture()
def mock_orient_client(mocker):
    mock_client = mocker.Mock(spec=OrientDB)

    mock_client.query.return_value = [{"key": "value"}, {"key": "value"}]
    mock_client.command.return_value = [OrientRecord(content={"__rid": "#12:0"}), ]
    mock_client.record_delete.return_value = True
    mock_client.record_create.return_value = [12]

    return mock_client


@pytest.fixture(autouse=True)
def patch_orient_client(monkeypatch, mock_orient_client):
    def fake_orient_client(*args, **kwargs):
        return mock_orient_client

    monkeypatch.setattr(Orient, "__init__", fake_orient_client)
