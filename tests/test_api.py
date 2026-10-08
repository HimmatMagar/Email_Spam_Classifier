import pytest
from conftest import *

def test_home(client):
    r = client.get("/")
    assert r.status_code == 200
    assert "message" in r


def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    body = r.json()
    assert body['status'] is 'Ok'
    assert body['model_loaded'] is True


def test_predict_spam(client, sample_spam):
    r = client.post("/predict", json={'text': sample_spam})
    assert r.status_code == 200
    body = r.json()
    assert body['prediction'] in (0, 1)
    assert isinstance(body['prediction'], int)
    assert body["label"] in ("spam", "ham")


def test_predict_ham(client, sample_ham):
    r = client.post("/predict", json={"text": sample_ham})
    assert r.status_code == 200


def test_predict_missing_field(client):
    r = client.post("/predict", json={})
    assert r.status_code == 422


def test_predict_wrong_type(client):
    r = client.post("/predict", json={"text": 123})
    assert r.status_code == 422
