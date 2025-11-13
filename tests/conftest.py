"""Conftest."""

from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

from src.db.session import get_db
from src.main import app
from src.models.board import Board
from src.models.card import Card
from src.models.list import List  # noqa: F401

SQLALCHEMY_DATABASE_URL="sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

SQLModel.metadata.create_all(bind=engine)

@pytest.fixture
def db_session():
    """Create a new database session for each test."""
    connection = engine.connect()
    transaction = connection.begin()
    session = TestSessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def client(db_session):
    """FastAPI TestClient that shares the same DB session."""

    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()

board_payload = {
    "id":uuid4(),
    "title":"My Test Board",
    "org_id":"This is a test board",
    "image_id":"This is a test board",
    "image_thumb_url":"This is a test board",
    "image_full_url":"This is a test board",
    "image_user_name":"This is a test board",
    "image_link_html":"This is a test board",
}
list_payload = {
    "id":uuid4(),
    "title":"My Test Title",
    "board_id":board_payload["id"],
}

card_payload = {
    "id":uuid4(),
    "title":"My Test Title",
    "list_id":list_payload["id"],
}


@pytest.fixture
def board_model(db_session):
    """Test board."""
    board_test = Board(**board_payload)
    db_session.add(board_test)
    db_session.commit()
    db_session.refresh(board_test)
    return board_test


@pytest.fixture
def list_model(db_session):
    """Test list."""
    list_test = List(**list_payload)
    db_session.add(list_test)
    db_session.commit()
    db_session.refresh(list_test)
    return list_test

@pytest.fixture
def card_model(db_session):
    """Test card."""
    card_test = Card(**card_payload)
    db_session.add(card_test)
    db_session.commit()
    db_session.refresh(card_test)
    return card_test

@pytest.fixture(autouse=True)
def clean_tables(db_session):
    """Clean up tables after each test."""
    yield
    for table in reversed(SQLModel.metadata.sorted_tables):
        db_session.execute(table.delete())
    db_session.commit()
