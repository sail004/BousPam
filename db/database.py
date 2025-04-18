from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
#from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs


SQLALCHEMY_DATABASE_URL = "postgresql://postgres:pass@localhost/postgres" #"postgresql+asyncpg://postgres:pass@localhost/postgres"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
#, connect_args={"check_same_thread": False}
#async_session_maker = async_sessionmaker(engine, expire_on_commit=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
