import pytest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app
@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

# ✅ Test valid input
def test_valid_input(client):
    response = client.post("/categorise", json={
        "text": "There is high financial risk due to compliance failure"
    })
    assert response.status_code == 200
    data = response.get_json()
    assert "category" in data
    assert data["is_fallback"] is False

# ❌ Test empty input
def test_empty_input(client):
    response = client.post("/categorise", json={
        "text": ""
    })
    assert response.status_code == 400

# ❌ Test short input
def test_short_input(client):
    response = client.post("/categorise", json={
        "text": "Hi"
    })
    assert response.status_code == 400

# ❌ Test invalid JSON
def test_invalid_json(client):
    response = client.post("/categorise", data="invalid")
    assert response.status_code == 400