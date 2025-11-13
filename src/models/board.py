"""Board model."""

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from src.models.list import List


class Board(SQLModel, table=True):
    """Board model."""

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str = Field(max_length=255)
    org_id: str = Field(max_length=100, index=True)
    image_id: str | None = Field(max_length=100, nullable=True)
    image_thumb_url: str | None = Field(max_length=255, nullable=True)
    image_full_url: str | None = Field(max_length=255, nullable=True)
    image_user_name: str | None = Field(max_length=100, nullable=True)
    image_link_html: str | None = Field(max_length=255, nullable=True)
    created_at: datetime | None = Field(default=datetime.now(), nullable=True)
    updated_at: datetime | None = Field(default=datetime.now(), nullable=True)

    lists: list["List"] = Relationship(back_populates="board", cascade_delete=True)
