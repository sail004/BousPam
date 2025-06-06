from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from services import crud_utils
from services.crud_utils import get_current_user
from services.schemas.login import login_request, login_response
from db.database import SessionLocal
from fastapi import Response


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


login_router = APIRouter(prefix='/login', tags=['Login'])


@login_router.put(
    "/",
    response_model=login_response.ReturnOwnerOrEmployee,
    description="Operation for login employee or transport company's owner"
)
async def login(response: Response, auth_data: login_request.Login, db: Session = Depends(get_db)):
    db_employee = await crud_utils.login_employee(db, login=auth_data.login, password=auth_data.password)
    db_tc_owner = await crud_utils.login_transport_company_owner(db, login=auth_data.login, password=auth_data.password)
    if db_employee == 'numb' and db_tc_owner == 'numb':
        return login_response.ReturnOwnerOrEmployee(msg='Incorrect login')
    if db_employee == 'inc' or db_tc_owner == 'inc':
        return login_response.ReturnOwnerOrEmployee(msg='Incorrect password')
    if type(db_employee) != str:
        access_token = crud_utils.create_access_token({"sub": str(db_employee.id)})
    else:
        access_token = crud_utils.create_access_token({"sub": str(db_tc_owner.id)})
    response.set_cookie(key="users_access_token", value=access_token, httponly=True)
    return db_employee if type(db_employee) != str else db_tc_owner


@login_router.get(
    "/me",
    response_model=login_response.ReturnOwnerOrEmployee,
    description="Operation for getting current user by info in cookie"
)
async def get_me(user_data = Depends(get_current_user)):
    return user_data


@login_router.post(
    "/logout/",
    response_model=login_response.SuccessfulLogout,
    description="Operation for logout current user"
)
async def logout_user(response: Response):
    response.delete_cookie(key="users_access_token")
    return {'message': 'User successfully logout from system'}
