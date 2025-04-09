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
from app.tg import tg_router
from app.cards import card_router
from app.tc_owner import owner_router
from app.default import login_router
from app.buses import bus_router
from app.routes import route_router
from database import SessionLocal, engine
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.openapi.docs import get_swagger_ui_html


models.Base.metadata.create_all(bind=engine)

app = FastAPI(title='BousPam API')

@app.get("/", include_in_schema=False)
async def home():
    return RedirectResponse("/docs")

favicon_path = 'favicon.ico'
@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse(favicon_path)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/docs", include_in_schema=False)
async def swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="FastAPI",
        swagger_favicon_url="/favicon.png"
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

app.include_router(login_router)
app.include_router(user_router)
app.include_router(operations_router)
app.include_router(terminal_router)
app.include_router(company_router)
app.include_router(employee_router)
app.include_router(tg_router)
app.include_router(card_router)
app.include_router(owner_router)
app.include_router(bus_router)
app.include_router(route_router)
