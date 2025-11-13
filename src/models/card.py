"""Card model."""

import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from src.models.list import List

class Card(SQLModel, table=True):
    """Card model."""

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str = Field(max_length=255)
    order: int = Field(default=0)
    description: str | None
    list_id: uuid.UUID = Field(foreign_key="list.id", index=True, ondelete="CASCADE")
    created_at: datetime | None = Field(default=datetime.now(), nullable=True)
    updated_at: datetime | None = Field(default=datetime.now(), nullable=True)

    list: Optional["List"] = Relationship(back_populates="cards")
