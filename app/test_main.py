import pytest
from fastapi.testclient import TestClient

from app.main import app, config_store


@pytest.fixture(autouse=True)
def clear_config_store():
    config_store.clear()
    yield
    config_store.clear()


@pytest.fixture
def client():
    return TestClient(app)


def test_health_and_version(client):
    assert client.get("/health").json() == {"status": "ok"}
    assert client.get("/version").json() == {"version": "1.0.0"}


def test_environment_comes_from_environment_variable(client, monkeypatch):
    monkeypatch.setenv("ENVIRONMENT", "test")
    assert client.get("/env").json() == {"environment": "test"}


def test_config_can_be_created_read_and_deleted(client):
    item = {"name": "database_url", "value": "postgres://example"}

    assert client.post("/config", json=item).json() == item
    assert client.get("/config/database_url").json() == item
    assert client.delete("/config/database_url").json() == {"deleted": True}
    assert client.get("/config/database_url").status_code == 404


def test_missing_config_delete_is_idempotent(client):
    assert client.delete("/config/missing").json() == {"deleted": False}


def test_config_name_must_not_be_empty(client):
    response = client.post("/config", json={"name": "", "value": "value"})
    assert response.status_code == 422
