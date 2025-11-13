"""Board schema."""

import uuid
from datetime import datetime

from pydantic import BaseModel


class BoardBase(BaseModel):
    """Base Board Schema."""

    title: str
    org_id: str
    image_id: str
    image_thumb_url: str
    image_full_url: str
    image_user_name: str
    image_link_html: str


class BoardCreate(BoardBase):
    """Board Create Schema."""

    pass

class BoardUpdate(BoardBase):
    """Board Update Schema."""

    pass


class Board(BoardBase):
    """Board Schema."""

    id: uuid.UUID
    created_at: datetime | None = None
    updated_at: datetime | None = None
