from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_async_engine(
        "sqlite+aiosqlite:///test.db",
        echo=True,
    )

async_session = async_sessionmaker(engine, expire_on_commit=False)
Base = declarative_base()
