"""Test list."""

from uuid import uuid4

import pytest


def test_get_lists(client, list_model):
    """Test get lists."""
    response = client.get("/api/lists/")
    assert response.status_code == 200

    data = response.json()
    assert "data" in data
    assert isinstance(data["data"], list)
    assert len(data["data"]) > 0
    assert "id" in data["data"][0]
    assert data["data"][0]["title"] == list_model.title

def test_create_list(client, board_model):
    """Test create list."""
    payload: dict = {
        "title": "My Test List",
        "board_id": str(board_model.id),
    }
    response = client.post("/api/lists/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["data"]["title"] == payload["title"]
    assert "id" in data["data"]

def test_create_list_invalid(client):
    """Test create list invalid."""
    payload = {
        "title": 1,
    }

    response = client.post("/api/lists/", json=payload)
    assert response.status_code == 422


def test_update_list_success(client, list_model, board_model):
    """Test successful update list."""
    payload: dict = {
        "title": "My Test List",
        "board_id": str(board_model.id),
    }

    response = client.put(f"/api/lists/{list_model.id}", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["title"] == payload["title"]


def test_update_list_invalid(client, list_model):
    """Test update list invalid."""
    payload = {
        "title": 1,
    }

    response = client.put(f"/api/lists/{list_model.id}", json=payload)
    assert response.status_code == 422

def test_delete_list_success(client, list_model):
    """Test successful delete list."""
    response = client.delete(f"/api/lists/{list_model.id}")
    assert response.status_code == 200
    assert response.json()["message"] == "List deleted successfully"


def test_delete_list_not_found(client):
    """Test delete non-existent list returns 404."""
    fake_id = uuid4()
    response = client.delete(f"/api/lists/{fake_id}")
    assert response.status_code == 404
    assert "not found" in response.json()["message"].lower()


def test_not_found_board_id_when_create_list(client):
    """Test not found board id when create list."""
    fake_id = uuid4()
    payload: dict = {
        "title": "My Test List",
        "board_id": str(fake_id),
    }
    response = client.post("/api/lists/", json=payload)
    assert response.status_code == 404
