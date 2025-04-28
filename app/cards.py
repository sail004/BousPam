from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from services import crud_utils
from services.schemas.card import card_request, card_response
from db.database import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


card_router = APIRouter(prefix='/card', tags=['Interaction with cards'])


@card_router.post(
    "/create/",
    response_model=card_response.CardNumber,
    description="Operation for creating card"
)
async def create_card(card: card_request.CardCreate, db: Session = Depends(get_db)):
    db_user = await crud_utils.get_user_by_id(db, user_id=card.owner_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail=f"User with id=\'{card.owner_id}\' not found")
    return card_response.CardNumber(card_number=await crud_utils.create_card(db=db, card=card))


@card_router.get(
    "/get-list/",
    response_model=list[card_response.Card],
    description="Operation for getting list of cards"
)
async def read_cards(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    cards = await crud_utils.get_cards(db, skip=skip, limit=limit)
    return cards


@card_router.put(
    "/update/",
    response_model=card_response.Card,
    description="Operation for updating card by its id"
)
async def update_card_by_id(card_id: int, card: card_request.CardUpdate, db: Session = Depends(get_db)):
    db_card = await crud_utils.get_card_by_id(db, card_id=card_id)
    if db_card is None:
        raise HTTPException(status_code=404, detail=f"Card with id=\'{card_id}\' not found")
    return await crud_utils.update_card(db, card=card, card_id=card_id)


@card_router.delete(
    "/delete/by-id",
    response_model=card_response.SuccessfulDeletion,
    description="Operation for deleting card by its id"
)
async def delete_card_by_id(card_id: int, db: Session = Depends(get_db)):
    db_card = await crud_utils.get_card_by_id(db, card_id=card_id)
    if db_card is None:
        raise HTTPException(status_code=404, detail=f"Card with id=\'{card_id}\' not found")
    await crud_utils.delete_card(db, card_id=card_id)

    return {
        "status": "ok",
        "message": "Deletion was successful"
    }
