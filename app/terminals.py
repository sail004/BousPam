from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from services import crud_utils
from services.schemas.terminal import terminal_request, terminal_response
from db.database import SessionLocal
from services.api_key_verification import verify_api_key


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


terminal_router = APIRouter(prefix='/terminals', tags=['Interaction with terminals'])


@terminal_router.post(
    "/create/",
    response_model=terminal_response.ReturnTerminal,
    description="Operation for creating terminal"
)
async def create_terminal(terminal: terminal_request.TerminalCreate, db: Session = Depends(get_db)):
    db_tc = await crud_utils.get_transport_company_by_name(db, tc_name=terminal.company)
    if db_tc is None:
        raise HTTPException(status_code=404, detail=f"Transport company with name=\'{terminal.company}\' not found")
    return await crud_utils.create_terminal(db=db, terminal=terminal)


@terminal_router.get(
    "/get/by-id/",
    response_model=terminal_response.ReturnTerminal,
    description="Operation for getting terminal by its id"
)
async def read_terminal_by_id(terminal_id: int, db: Session = Depends(get_db)):
    db_term = await crud_utils.get_terminal_by_id(db, terminal_id=terminal_id)
    if db_term is None:
        raise HTTPException(status_code=404, detail=f"Terminal with id=\'{terminal_id}\' not found")
    return db_term


@terminal_router.get(
    "/get-list/",
    response_model=list[terminal_response.ReturnTerminal],
    description="Operation for getting list of all terminals"
)
async def read_terminals(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    terminals = await crud_utils.get_terminals(db, skip=skip, limit=limit)
    return terminals


@terminal_router.get(
    "/get/by-company/",
    response_model=list[terminal_response.ReturnTerminal],
    description="Operation for getting list of terminals owned by a company, by the name of that company"
)
async def read_terminals_by_company_name(company: str, db: Session = Depends(get_db)):
    db_term = await crud_utils.get_terminals_by_company(db, company_name=company)
    if db_term is None:
        raise HTTPException(status_code=404, detail=f"Transport company with name=\'{company}\' not found")
    return db_term


@terminal_router.put(
    "/update/",
    response_model=terminal_response.ReturnTerminal,
    description="Operation for updating terminal by its id"
)
async def update_terminal_by_id(terminal_id: int, term: terminal_request.TerminalUpdate, db: Session = Depends(get_db)):
    db_term = await crud_utils.get_terminal_by_id(db, terminal_id=terminal_id)
    if db_term is None:
        raise HTTPException(status_code=404, detail=f"Terminal with id=\'{terminal_id}\' not found")
    return await crud_utils.update_terminal(db, term=term, term_id=terminal_id)


@terminal_router.delete(
    "/delete/",
    response_model=terminal_response.SuccessfulDeletion,
    description="Operation for deleting terminal by its id"
)
async def delete_terminal_by_id(terminal_id: int, db: Session = Depends(get_db)):
    db_term = await crud_utils.get_terminal_by_id(db, terminal_id=terminal_id)
    if db_term is None:
        raise HTTPException(status_code=404, detail=f"Terminal with id=\'{terminal_id}\' not found")
    await crud_utils.delete_terminal(db, terminal_id=terminal_id)

    return {
        "status": "ok",
        "message": "Deletion was successful"
    }

@terminal_router.get(
    "/get-stoplist/",
    response_model=list,
    description="Operation for getting stoplist"
)
async def read_stoplist(api_key: str = Depends(verify_api_key), db: Session = Depends(get_db)):
    if api_key:
        stoplist = await crud_utils.get_stoplist(db)
        re = [card.card_number for card in stoplist]
        return re
