from datetime import datetime, timedelta, timezone
from fastapi import Depends, FastAPI, HTTPException, APIRouter
from sqlalchemy.orm import Session
import os
import crud_utils
import models
import schemas
from app.employee import employee_router
from app.company import company_router
from app.users import user_router
from app.terminals import terminal_router
from app.operations import operations_router
from database import SessionLocal, engine
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

root = os.path.dirname(os.path.abspath(__file__))
#app.mount("/static", StaticFiles(directory="static"), name="static")

#@app.get("/login/") #, response_model=List[schemas.Product]
#def login_user(phone_number: str, password: str, db: Session = Depends(get_db)):
#    db_user = crud_utils.login_user(db, phone_number=phone_number, password=password)
#    if db_user == 'numb':
#        return 'Incorrect phone number'
#    if db_user == 'inc':
#        return 'Incorrect password'
#    return db_user

app.include_router(user_router)
app.include_router(operations_router)
app.include_router(terminal_router)
app.include_router(company_router)
app.include_router(employee_router)
