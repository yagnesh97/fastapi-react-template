from fastapi.testclient import TestClient

from app.main import app
from app.utilities.static_values import RATE_LIMIT_EXCEED

client = TestClient(app)

BASE_PATH = "/v1/utils"


def test_api_status() -> None:
    """
    Test API status
    """
    r = client.get(f"{BASE_PATH}/api-status")
    assert r.status_code == 200
    assert r.json()["status"] == "success"


def test_rate_limit() -> None:
    """
    Test rate limiting functionality
    """
    # Send 100 requests to test the rate limit
    for _ in range(100):
        r = client.get(f"{BASE_PATH}/api-status")
        assert r.status_code == 200  # Expect success response for the first 99 requests

    # Send a 100th request to trigger rate limit exceeded
    r = client.get(f"{BASE_PATH}/api-status")
    assert r.status_code == 429  # Expect rate limit exceeded response
    assert r.json()["detail"] == RATE_LIMIT_EXCEED
