from api.app import app
from fastapi.testclient import TestClient

client = TestClient(app=app)

def test_health():
    assert client.get("/health").status_code == 200

def test_predict_spam():
    r = client.post("/predict", json={"text": "You won a free iPhone, click now!!!"})
    assert r.status_code == 200
    body = r.json()
    assert body["label"] in ("spam", "ham")
    assert 0 <= body["confidence"] <= 1

def test_predict_rejects_missing_text():
    assert client.post("/predict", json={}).status_code == 422


def test_predict_empty_text():
    r = client.post("/predict", json={"text": ""})
    assert r.status_code in (200, 422) 