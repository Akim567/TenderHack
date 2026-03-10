import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client() -> TestClient:
    """HTTP client fixture for API tests."""
    with TestClient(app) as test_client:
        yield test_client
