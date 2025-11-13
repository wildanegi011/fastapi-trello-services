"""Test board."""

from uuid import uuid4

payload: dict = {
    "title": "My Test Board",
    "org_id": "This is a test board",
    "image_id": "This is a test board",
    "image_thumb_url": "This is a test board",
    "image_full_url": "This is a test board",
    "image_user_name": "This is a test board",
    "image_link_html": "This is a test board",
}

def test_get_boards(client, board_model):
    """Test get boards."""
    response = client.get("/api/boards/")
    assert response.status_code == 200

    data = response.json()
    assert "data" in data
    assert isinstance(data["data"], list)
    assert len(data["data"]) > 0
    assert "id" in data["data"][0]
    assert data["data"][0]["title"] == board_model.title

def test_create_board(client):
    """Test create board."""
    response = client.post("/api/boards/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["data"]["title"] == payload["title"]
    assert "id" in data["data"]

def test_create_board_invalid(client):
    """Test create board invalid."""
    payload = {
        "title": 1,
    }

    response = client.post("/api/boards/", json=payload)
    assert response.status_code == 422


def test_update_board_success(client, board_model):
    """Test successful update board."""
    response = client.put(f"/api/boards/{board_model.id}", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["title"] == payload["title"]


def test_update_board_invalid(client, board_model):
    """Test update board invalid."""
    payload = {
        "title": 1,
    }

    response = client.put(f"/api/boards/{board_model.id}", json=payload)
    assert response.status_code == 422

def test_delete_board_success(client, board_model):
    """Test successful delete board."""
    response = client.delete(f"/api/boards/{board_model.id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Board deleted successfully"


def test_delete_board_not_found(client):
    """Test delete non-existent board returns 404."""
    fake_id = uuid4()
    response = client.delete(f"/api/boards/{fake_id}")
    assert response.status_code == 404
    assert "not found" in response.json()["message"].lower()
