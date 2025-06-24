from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import registry

from .settings import settings

Base = registry()

engine = create_async_engine(settings.DATABASE_URL)


async def get_session():
    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session


T_Session = Annotated[AsyncSession, Depends(get_session)]
