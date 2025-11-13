"""Card Service."""

from uuid import UUID

from sqlalchemy.orm import Session

from src.models.card import Card
from src.schemas.card import CardCreate, CardUpdate
from src.services.list import ListService


class CardService:
    """Card Service."""

    def __init__(self, db: Session) -> None:
        """Initialize."""
        self.db = db
        self.list_service = ListService(db)

    def get_cards(self, page: int = 1, limit: int = 10) -> tuple[list[Card], int]:
        """Get cards service."""
        skip = (page - 1) * limit
        query = self.db.query(Card)
        total = query.count()
        cards = query.offset(skip).limit(limit).all()
        return cards, total

    def get_card_by_id(self, card_id: UUID) -> Card:
        """Get card by id service."""
        card = self.db.query(Card).filter(Card.id == card_id).first()
        if not card:
            raise ValueError("Card not found")
        return card

    def create_card(self, card_schema: CardCreate) -> Card:
        """Create card service."""
        self.list_service.get_list_by_id(card_schema.list_id)

        db_card = Card(**card_schema.model_dump())
        self.db.add(db_card)
        try:
            self.db.commit()
        except Exception:
            self.db.rollback()
            raise
        self.db.refresh(db_card)
        return db_card

    def update_card(self, card_id: UUID, card_schema: CardUpdate) -> Card:
        """Update card service."""
        self.list_service.get_list_by_id(card_schema.list_id)

        card = self.get_card_by_id(card_id)
        for key, value in card_schema.model_dump().items():
            setattr(card, key, value)
        self.db.add(card)
        try:
            self.db.commit()
        except Exception:
            self.db.rollback()
            raise
        self.db.refresh(card)
        return card

    def delete_card(self, card_id: UUID) -> None:
        """Delete card service."""
        card = self.get_card_by_id(card_id)
        self.db.delete(card)
        self.db.commit()
