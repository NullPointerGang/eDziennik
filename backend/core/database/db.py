from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from typing import AsyncGenerator
from core.config import config
from core.database.base import Base
from sqlalchemy import select
from app.user.schemas.role_schem import Roles


engine = create_async_engine(config.database.connect_string)

async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Получает асинхронную сессию базы данных.

    Используется как зависимость FastAPI для работы с базой данных.

    Возвращает:
        AsyncGenerator[AsyncSession, None]: Асинхронный генератор сессий SQLAlchemy.
    """
    async with async_session_maker() as session:
        yield session

async def init_db():
    """
    Инициализирует базу данных.

    Создаёт все таблицы, описанные в метаданных SQLAlchemy.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def seed_roles() -> None:
    """
    Создаёт базовые роли, если их нет: "student", "teacher".
    """
    async with async_session_maker() as session:  # type: AsyncSession
        for role_name in ("student", "teacher"):
            result = await session.execute(select(Roles).where(Roles.name == role_name))
            role = result.scalars().first()
            if role is None:
                session.add(Roles(name=role_name))
        await session.commit()
