from datetime import datetime, date, time, timedelta

from fastapi import FastAPI, Depends
import os
from db import models
from app.employee import employee_router
from app.company import company_router
from app.users import user_router
from app.terminals import terminal_router
from app.operations import operations_router
from app.tg import tg_router
from app.cards import card_router
from app.tc_owner import owner_router
from app.login import login_router
from app.buses import bus_router
from app.routes import route_router
from app.places import place_router
from db.database import engine, SessionLocal
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.responses import RedirectResponse
from fastapi.openapi.docs import get_swagger_ui_html
from db.models import Queue
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from services import crud_utils

models.Base.metadata.create_all(bind=engine)

root = os.path.dirname(os.path.abspath(__file__))
app = FastAPI(title='BousPam API', docs_url=None)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def move_queues():
    crud_utils.delete_expired_queues(db = Depends(get_db))
    crud_utils.add_new_queue_day(db = Depends(get_db))


scheduler = BackgroundScheduler()

scheduler.add_job(
    move_queues,
    trigger=CronTrigger(hour=23, minute=0),
)


@app.on_event('startup')
async def startup():
    db = SessionLocal()
    try:
        if not db.query(Queue).first():
            db.add_all([
                Queue(status="free", date=(date.today() + timedelta(days=j)), time=time(hour=(i // 15), minute=(i % 15))) for i in range(36, 85) for j in range(3)
            ])
            db.commit()
    finally:
        db.close()
    scheduler.start()


@app.on_event("shutdown")
async def shutdown_event():
    scheduler.shutdown()


@app.get("/", include_in_schema=False)
async def home():
    return RedirectResponse("/docs")


favicon_path = 'static/favicon.ico'
@app.get('/static/favicon.ico', include_in_schema=False)
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
async def overriden_swagger():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="FastAPI",
        swagger_favicon_url=favicon_path
    )


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
app.include_router(place_router)
