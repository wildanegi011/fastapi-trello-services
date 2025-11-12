"""Conftest."""

from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

from src.db.session import get_db
from src.main import app
from src.models.board import Board  # noqa: F401

SQLALCHEMY_DATABASE_URL="sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

SQLModel.metadata.create_all(bind=engine)

def override_get_db():
    """Test session."""
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="session")
def client():
    """Test client."""
    with TestClient(app) as c:
        yield c

@pytest.fixture
def db_session():
    """Test session."""
    return next(override_get_db())

@pytest.fixture
def board(db_session):
    """Test board."""
    board = Board(
        id=uuid4(),
        title="My Test Board",
        org_id="This is a test board",
        image_id="This is a test board",
        image_thumb_url="This is a test board",
        image_full_url="This is a test board",
        image_user_name="This is a test board",
        image_link_html="This is a test board",
    )
    db_session.add(board)
    db_session.commit()
    return board
