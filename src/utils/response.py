"""Response utils."""

from typing import Any

from src.schemas.response import Metadata, ResponseSchema


def success_response(data: Any = None, message: str = "Success") -> ResponseSchema:
    """Success response."""
    return ResponseSchema(status="success", message=message, data=data)

def error_response(message: str) -> ResponseSchema:
    """Error response."""
    return ResponseSchema(status="error", message=message)

def paginated_response(
    data: Any = None,
    message: str = "Success",
    page: int = 1,
    limit: int = 10,
    total: int = 0,
) -> ResponseSchema:
    """Paginated response."""
    total_pages = (total + limit - 1) // limit if limit > 0 else 1
    return ResponseSchema(
        status="success",
        message=message,
        data=data,
        metadata=Metadata(
            page=page,
            limit=limit,
            total=total,
            total_pages=total_pages,
        ),
    )
