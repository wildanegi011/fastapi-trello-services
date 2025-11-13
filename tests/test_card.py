"""Test card."""

from uuid import uuid4


def test_get_cards(client, card_model):
    """Test get cards."""
    response = client.get("/api/cards/")
    assert response.status_code == 200

    data = response.json()
    assert "data" in data
    assert isinstance(data["data"], list)
    assert len(data["data"]) > 0
    assert "id" in data["data"][0]
    assert data["data"][0]["title"] == card_model.title

def test_create_card(client, list_model):
    """Test create card."""
    payload: dict = {
        "title": "My Test Card",
        "list_id": str(list_model.id)
    }
    response = client.post("/api/cards/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["data"]["title"] == payload["title"]
    assert "id" in data["data"]

def test_create_card_invalid(client):
    """Test create card invalid."""
    payload = {
        "title": 1,
    }

    response = client.post("/api/cards/", json=payload)
    assert response.status_code == 422


def test_update_card_success(client, card_model, list_model):
    """Test successful update card."""
    payload: dict = {
        "title": "My Test Card",
        "list_id": str(list_model.id),
    }

    response = client.put(f"/api/cards/{card_model.id}", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["title"] == payload["title"]


def test_update_card_invalid(client, card_model):
    """Test update card invalid."""
    payload = {
        "title": 1,
    }

    response = client.put(f"/api/cards/{card_model.id}", json=payload)
    assert response.status_code == 422

def test_delete_card_success(client, card_model):
    """Test successful delete card."""
    response = client.delete(f"/api/cards/{card_model.id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Card deleted successfully"


def test_delete_card_not_found(client):
    """Test delete non-existent card returns 404."""
    fake_id = uuid4()
    response = client.delete(f"/api/cards/{fake_id}")
    assert response.status_code == 404
    assert "not found" in response.json()["message"].lower()


def test_not_found_board_id_when_create_card(client):
    """Test not found board id when create card."""
    fake_id = uuid4()
    payload: dict = {
        "title": "My Test Card",
        "list_id": str(fake_id),
        "board_id": str(fake_id),
    }
    response = client.post("/api/cards/", json=payload)
    assert response.status_code == 404

