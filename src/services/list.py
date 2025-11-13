"""List Service."""

from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.models.board import Board
from src.models.list import List
from src.schemas.list import ListCreate, ListUpdate
from src.services.board import BoardService


class ListService:
    """List Service."""

    def __init__(self, db: Session) -> None:
        """Initialize."""
        self.db = db
        self.board_service = BoardService(db)

    def get_lists(self, page: int = 1, limit: int = 10) -> tuple[list[List], int]:
        """Get lists service."""
        skip = (page - 1) * limit
        query = self.db.query(List)
        total = query.count()
        lists = query.offset(skip).limit(limit).all()
        return lists, total

    def get_list_by_id(self, list_id: UUID) -> List:
        """Get list by id service."""
        list = self.db.query(List).filter(List.id == list_id).first()
        if not list:
            raise ValueError("List not found")
        return list

    def create_list(self, list_schema: ListCreate) -> List:
        """Create list service."""
        # Ensure the board exists
        self.board_service.get_board_by_id(list_schema.board_id)

        db_list = List(**list_schema.model_dump())
        self.db.add(db_list)
        try:
            self.db.commit()
        except Exception:
            self.db.rollback()
            raise
        self.db.refresh(db_list)
        return db_list

    def update_list(self, list_id: UUID, list_schema: ListUpdate) -> List:
        """Update list service."""
        # Ensure the board exists
        self.board_service.get_board_by_id(list_schema.board_id)

        list = self.get_list_by_id(list_id)
        for key, value in list_schema.model_dump().items():
            setattr(list, key, value)
        self.db.add(list)
        try:
            self.db.commit()
        except Exception:
            self.db.rollback()
            raise
        self.db.refresh(list)
        return list

    def delete_list(self, list_id: UUID) -> None:
        """Delete list service."""
        list = self.get_list_by_id(list_id)
        self.db.delete(list)
        self.db.commit()
