from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from services import crud_utils, luhn
from services.schemas.operations import operations_request, operations_response
from db.database import SessionLocal
from services.api_key_verification import verify_api_key


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


operations_router = APIRouter(prefix='/operations', tags=['Interaction with transactions'])


@operations_router.get(
    "/getlist/",
    response_model=list[operations_response.ReturnOperation],
    description="Operation for getting list of all operations"
)
async def read_operations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    operations = await crud_utils.get_operations(db, skip=skip, limit=limit)
    return operations


@operations_router.get(
    "/get/by-terminal-id/",
    response_model=list[operations_response.ReturnOperation],
    description="Operation for getting list of operations by id of terminal that provided these operations"
)
async def read_operations_by_terminal_id(terminal_id: int, db: Session = Depends(get_db)):
    db_ops = await crud_utils.get_operations_by_terminal_id(db, term_id=terminal_id)
    if db_ops is None:
        raise HTTPException(status_code=404, detail=f"Terminal with id=\'{terminal_id}\' not found")
    return db_ops


@operations_router.get(
    "/get/by-user-id/",
    response_model=list[operations_response.ReturnOperation],
    description="Operation for getting list of operations by id of user with whose account these operations were performed"
)
async def read_operations_by_user_id(user_id: int, db: Session = Depends(get_db)):
    db_ops = await crud_utils.get_operations_by_user_id(db, user_id=user_id)
    if db_ops is None:
        raise HTTPException(status_code=404, detail=f"User with id=\'{user_id}\' not found")
    return db_ops


@operations_router.put(
    "/payment/",
    response_model=operations_response.ReturnBalance,
    description="Operation for payment by user's card number, providing by terminal"
)
async def payment_by_card_number(operation: operations_request.OperationPaymentCreate, api_key: str = Depends(verify_api_key), db: Session = Depends(get_db)):
    if api_key:
        db_card = await crud_utils.get_card_by_number(db, card_number=operation.card_number)
        db_terminal = await crud_utils.get_terminal_by_id(db, terminal_id=operation.id_terminal)
        if db_terminal is None:
            raise HTTPException(status_code=404, detail=f"Terminal with id=\'{operation.id_terminal}\' not found")
        if db_card is None:
            raise HTTPException(status_code=404, detail=f"Card with number=\'{operation.card_number}\' not found")
        if db_terminal.hash != operation.terminal_hash:
            raise HTTPException(status_code=404, detail=f"Incorrect terminal hash")
        db_user = await crud_utils.get_user_by_id(db, db_card.owner_id)
        delta_time = datetime.now() - operation.request_time.replace(tzinfo=None)
        #crud_utils.create_operation_payment(db, operation, 'payment')
        balance_change = await crud_utils.get_price_by_terminal_id(db, operation.id_terminal)
        if delta_time < timedelta(minutes=1):
            if db_user.balance < abs(balance_change):
                raise HTTPException(status_code=400, detail=f"Insufficient funds to make the payment")
        new_balance = await crud_utils.create_operation_payment(db, operation, 'payment', db_card.owner_id)
        if new_balance < 0:
            await crud_utils.add_to_stoplist(db, operations_request.StopListCreate(
                card_number=operation.card_number,
                owner_id=db_user.id,
                owner_phone_number=db_user.phone_number
            ))
        return operations_response.ReturnBalance(balance=new_balance)


@operations_router.put(
    "/replenishment/",
    response_model=operations_response.ReturnBalance,
    description="Operation for replenishment by user's card number, providing by cashier(B2C-manager)"
)
async def replenishment_by_card_number(operation: operations_request.OperationReplenishmentCreate, db: Session = Depends(get_db)):
    db_card = await crud_utils.get_card_by_number(db, operation.card_number)
    if not await luhn.check(operation.card_number):
        return "Incorrect card number"
    if db_card is None:
        return f"Card with number=\'{operation.card_number}\' not found"
    db_user = await crud_utils.get_user_by_id(db, user_id=db_card.owner_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail=f"User with id=\'{db_card.owner_id}\' not found")
    new_balance = await crud_utils.create_operation_replenishment(db, operation, 'replenishment', db_card.owner_id)
    if new_balance > 0:
        await crud_utils.delete_from_stoplist(db, operation.card_number)
    return operations_response.ReturnBalance(balance=new_balance)


@operations_router.put(
    "/check-operations/",
    description="Operation for checking operations and record the discrepancy, if any. It is performed when the cashier logs in and out of the account"
)
async def check_operations(cashbox: operations_request.CheckOperations, db: Session = Depends(get_db)):
    db_cashier = await crud_utils.get_employee_by_id(db, cashbox.cashier_id)
    if db_cashier is None:
        raise HTTPException(status_code=404, detail=f"Employee with id=\'{cashbox.cashier_id}\' not found")
    await crud_utils.check_operations(db, cashbox)
