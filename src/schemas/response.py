"""Response Schema."""


from typing import Any, Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")

class Metadata(BaseModel):
    """Metadata."""

    page: int
    limit: int
    total: int
    total_pages: int | None = None
    extra: Any | None = None  # for filters, sort, etc.

class ResponseSchema(BaseModel, Generic[T]):  # noqa: UP046
    """Response Schema."""

    status: str
    message: str | None = None
    data: T | None = None
    metadata: Metadata | None = None
