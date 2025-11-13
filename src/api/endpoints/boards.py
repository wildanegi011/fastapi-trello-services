"""Endpoint Board."""

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from src.db.session import get_db
from src.schemas.board import Board as BoardSchema
from src.schemas.board import BoardCreate, BoardUpdate
from src.schemas.response import ResponseSchema
from src.services.board import BoardService
from src.utils.response import paginated_response, success_response

router = APIRouter()

def get_board_service(db: Annotated[Session, Depends(get_db)]):
    """Get board service."""
    return BoardService(db)


@router.get("/", response_model=ResponseSchema[list[BoardSchema]])
async def get_boards(
    service: Annotated[BoardService, Depends(get_board_service)],
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100)):
    """Get boards."""
    boards, total = service.get_boards(page, limit)
    return paginated_response(
        data=boards,
        message="Boards retrieved successfully",
        page=page,
        limit=limit,
        total=total,
    )


@router.get("/{board_id}", response_model=ResponseSchema[BoardSchema])
async def get_board_by_id(
    board_id: UUID,
    service: Annotated[BoardService, Depends(get_board_service)],
):
    """Get board by id."""
    board = service.get_board_by_id(board_id)
    return success_response(
        data=board,
        message="Board retrieved successfully",
    )


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_board(
    board: BoardCreate,
    service: Annotated[BoardService, Depends(get_board_service)],
):
    """Create board."""
    board = service.create_board(board)
    return success_response(
        data=board,
        message="Board created successfully",
    )

@router.put("/{board_id}")
async def update_board(
    board_id: UUID,
    board: BoardUpdate,
    service: Annotated[BoardService, Depends(get_board_service)],
):
    """Update board."""
    board = service.update_board(board_id, board)
    return success_response(
        data=board,
        message="Board updated successfully",
    )


@router.delete("/{board_id}")
async def delete_board(
    board_id: UUID,
    service: Annotated[BoardService, Depends(get_board_service)],
):
    """Delete board."""
    service.delete_board(board_id)
    return success_response(
        message="Board deleted successfully",
    )
