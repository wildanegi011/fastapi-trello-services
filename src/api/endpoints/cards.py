"""Endpoint Card."""

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from src.db.session import get_db
from src.schemas.card import Card as CardSchema
from src.schemas.card import CardCreate, CardUpdate
from src.schemas.response import ResponseSchema
from src.services.card import CardService
from src.utils.response import paginated_response, success_response

router = APIRouter()

def get_card_service(db: Annotated[Session, Depends(get_db)]):
    """Get card service."""
    return CardService(db)


@router.get("/", response_model=ResponseSchema[list[CardSchema]])
async def get_cards(
    service: Annotated[CardService, Depends(get_card_service)],
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100)):
    """Get cards."""
    cards, total = service.get_cards(page, limit)
    return paginated_response(
        data=cards,
        message="Cards retrieved successfully",
        page=page,
        limit=limit,
        total=total,
    )


@router.get("/{card_id}", response_model=ResponseSchema[CardSchema])
async def get_card_by_id(
    card_id: UUID,
    service: Annotated[CardService, Depends(get_card_service)],
):
    """Get card by id."""
    card = service.get_card_by_id(card_id)
    return success_response(
        data=card,
        message="Card retrieved successfully",
    )


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_card(
    card: CardCreate,
    service: Annotated[CardService, Depends(get_card_service)],
):
    """Create card."""
    card = service.create_card(card)
    return success_response(
        data=card,
        message="Card created successfully",
    )

@router.put("/{card_id}")
async def update_card(
    card_id: UUID,
    card: CardUpdate,
    service: Annotated[CardService, Depends(get_card_service)],
):
    """Update card."""
    card = service.update_card(card_id, card)
    return success_response(
        data=card,
        message="Card updated successfully",
    )


@router.delete("/{card_id}")
async def delete_card(
    card_id: UUID,
    service: Annotated[CardService, Depends(get_card_service)],
):
    """Delete card."""
    service.delete_card(card_id)
    return success_response(
        message="Card deleted successfully",
    )
