"""Endpoint List."""

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from src.db.session import get_db
from src.schemas.list import List as ListSchema
from src.schemas.list import ListCreate, ListUpdate
from src.schemas.response import ResponseSchema
from src.services.list import ListService
from src.utils.response import paginated_response, success_response

router = APIRouter()

def get_list_service(db: Annotated[Session, Depends(get_db)]):
    """Get list service."""
    return ListService(db)


@router.get("/", response_model=ResponseSchema[list[ListSchema]])
async def get_lists(
    service: Annotated[ListService, Depends(get_list_service)],
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100)):
    """Get lists."""
    lists, total = service.get_lists(page, limit)
    return paginated_response(
        data=lists,
        message="Lists retrieved successfully",
        page=page,
        limit=limit,
        total=total,
    )


@router.get("/{list_id}", response_model=ResponseSchema[ListSchema])
async def get_list_by_id(
    list_id: UUID,
    service: Annotated[ListService, Depends(get_list_service)],
):
    """Get list by id."""
    list = service.get_list_by_id(list_id)
    return success_response(
        data=list,
        message="List retrieved successfully",
    )


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_list(
    list: ListCreate,
    service: Annotated[ListService, Depends(get_list_service)],
):
    """Create list."""
    list = service.create_list(list)
    return success_response(
        data=list,
        message="List created successfully",
    )

@router.put("/{list_id}")
async def update_list(
    list_id: UUID,
    list: ListUpdate,
    service: Annotated[ListService, Depends(get_list_service)],
):
    """Update list."""
    list = service.update_list(list_id, list)
    return success_response(
        data=list,
        message="List updated successfully",
    )


@router.delete("/{list_id}")
async def delete_list(
    list_id: UUID,
    service: Annotated[ListService, Depends(get_list_service)],
):
    """Delete list."""
    service.delete_list(list_id)
    return success_response(
        message="List deleted successfully",
    )
