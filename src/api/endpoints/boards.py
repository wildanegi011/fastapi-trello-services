"""Endpoint Board."""

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from src.db.session import get_db
from src.schemas.board import BoardCreate
from src.services.board import BoardService
from src.utils.response import paginated_response, success_response

router = APIRouter()

def get_board_service(db: Annotated[Session, Depends(get_db)]):
    """Get board service."""
    return BoardService(db)

@router.get("/")
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


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_board(board: BoardCreate, service: Annotated[BoardService, Depends(get_board_service)]):
    """Create board."""
    board = service.create_board(board)
    return success_response(
        data=board,
        message="Board created successfully",
    )

@router.delete("/{board_id}")
async def delete_board(board_id: UUID, service: Annotated[BoardService, Depends(get_board_service)]):
    """Delete board."""
    service.delete_board(board_id)
    return success_response(message="Board deleted successfully")
