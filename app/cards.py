from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from services import crud_utils, schemas
from db.database import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


card_router = APIRouter(prefix='/card', tags=['Interaction with cards'])


@card_router.post("/create/") #, response_model=schemas.ProductCreate
async def create_card(card: schemas.CardCreate, db: Session = Depends(get_db)):
    db_user = await crud_utils.get_user_by_id(db, user_id=card.owner_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail=f"User with id=\'{card.owner_id}\' not found")
    return await crud_utils.create_card(db=db, card=card)


@card_router.get("/get-list/") #, response_model=List[schemas.Product]
async def read_cards(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    cards = await crud_utils.get_cards(db, skip=skip, limit=limit)
    return cards


@card_router.put("/update/") #, response_model=schemas.Product
async def update_card_by_id(card_id: int, card: schemas.CardUpdate, db: Session = Depends(get_db)):
    db_card = await crud_utils.get_card_by_id(db, card_id=card_id)
    if db_card is None:
        raise HTTPException(status_code=404, detail=f"Card with id=\'{card_id}\' not found")
    return await crud_utils.update_card(db, card=card, card_id=card_id)


@card_router.delete("/delete/by-id") #, response_model=dict
async def delete_card_by_id(card_id: int, db: Session = Depends(get_db)):
    db_card = await crud_utils.get_card_by_id(db, card_id=card_id)
    if db_card is None:
        raise HTTPException(status_code=404, detail=f"Card with id=\'{card_id}\' not found")
    await crud_utils.delete_card(db, card_id=card_id)

    return {
        "status": "ok",
        "message": "Deletion was successful"
    }
