"""Board schema."""

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
