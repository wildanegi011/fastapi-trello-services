"""Card schema."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class CardBase(BaseModel):
    """Base Card Schema."""

    title: str
    list_id: UUID


class CardCreate(CardBase):
    """Card Create Schema."""

    pass

class CardUpdate(CardBase):
    """Card Update Schema."""

    pass


class Card(CardBase):
    """Card Schema."""

    id: UUID
    order: int
    created_at: datetime
    updated_at: datetime | None = None
