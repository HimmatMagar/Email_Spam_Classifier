import pytest
from api.app import app
from fastapi.testclient import TestClient

@pytest.fixture(scope="session")
def client():
    with TestClient(app) as c:
        yield c

@pytest.fixture
def sample_spam():
    return "Congratulations! You've won a free iPhone. Click here to claim now!!!"


@pytest.fixture
def sample_ham():
    return "Hi team, the meeting tomorrow is moved to 3 PM. See you there."