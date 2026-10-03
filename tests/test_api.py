from api.app import app
from fastapi.testclient import TestClient

client = TestClient(app=app)

def test_health():
    assert client.get("/health").status_code == 200