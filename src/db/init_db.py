"""Initial database."""

from sqlmodel import SQLModel

from src.db.session import engine
from src.models.board import Board  # noqa: F401
from src.models.card import Card  # noqa: F401
from src.models.list import List  # noqa: F401


def init_db():
    """Initialize the database."""
    SQLModel.metadata.create_all(bind=engine)
    print("Database tables created successfully!")


if __name__ == "__main__":
    init_db()
