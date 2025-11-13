"""List model."""

import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from src.models.board import Board
    from src.models.card import Card


class List(SQLModel, table=True):
    """List model."""

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str = Field(max_length=255)
    order: int = Field(default=0)
    board_id: uuid.UUID = Field(foreign_key="board.id", index=True, ondelete="CASCADE")
    created_at: datetime | None = Field(default=datetime.now(), nullable=True)
    updated_at: datetime | None = Field(default=datetime.now(), nullable=True)

    board: Optional["Board"] = Relationship(back_populates="lists")
    cards: list["Card"] = Relationship(back_populates="list", cascade_delete=True)
