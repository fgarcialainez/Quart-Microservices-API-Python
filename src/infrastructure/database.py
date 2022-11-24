import os

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import NullPool

host = os.getenv("DB_HOST")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASS")
port = int(os.getenv("DB_PORT"))
dbname = os.getenv("DB_NAME")

engine = create_async_engine(
    f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{dbname}",
    echo=True,
    future=True,
    poolclass=NullPool
)
session_factory = sessionmaker(engine, class_=AsyncSession)
Base = declarative_base()
