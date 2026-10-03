import pytest
from fastapi.testclient import TestClient
from api.app import app

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:      # runs startup/lifespan, loads the model
        yield c

def test_health(client):
    assert client.get("/health").status_code == 200

def test_predict_spam(client):
    r = client.post("/predict", json={"text": "You won a free iPhone, click now!!!"})
    assert r.status_code == 200
    body = r.json()
    assert body["prediction"] in (0, 1)
    assert body["label"] in ("spam", "ham")

def test_predict_rejects_missing_text(client):
    assert client.post("/predict", json={}).status_code == 422