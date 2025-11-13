"""List schema."""

import uuid
from datetime import datetime

from pydantic import BaseModel

from src.schemas.board import Board


class ListBase(BaseModel):
    """Base List Schema."""

    title: str
    board_id: uuid.UUID

class ListCreate(ListBase):
    """List Create Schema."""

    pass

class ListUpdate(ListBase):
    """List Update Schema."""

    pass


class List(ListBase):
    """List Schema."""

    id: uuid.UUID
    order: int
    board: Board | None = None
    created_at: datetime
    updated_at: datetime | None = None
