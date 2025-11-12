"""Board Service."""

from uuid import UUID

from sqlalchemy.orm import Session

from src.models.board import Board
from src.schemas.board import BoardCreate


class BoardService:
    """Board Service."""

    def __init__(self, db: Session) -> None:
        """Initialize."""
        self.db = db

    def get_boards(self, page: int = 1, limit: int = 10) -> tuple[list[Board], int]:
        """Get boards service."""
        skip = (page - 1) * limit
        query = self.db.query(Board)
        total = query.count()
        boards = query.offset(skip).limit(limit).all()
        return boards, total

    def create_board(self, board: BoardCreate) -> Board:
        """Create board service."""
        db_board = Board(**board.model_dump())
        self.db.add(db_board)
        try:
            self.db.commit()
        except Exception:
            self.db.rollback()
            raise
        self.db.refresh(db_board)
        return db_board

    def delete_board(self, board_id: UUID) -> None:
        """Delete board service."""
        board = self.db.query(Board).filter(Board.id == board_id).first()
        if not board:
            raise ValueError("Board not found")
        self.db.delete(board)
        self.db.commit()
