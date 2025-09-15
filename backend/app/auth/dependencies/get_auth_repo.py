from fastapi import Depends
from app.auth.repositories.auth_repo import AuthRepo
from core.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession


def get_auth_repo(db: AsyncSession = Depends(get_db)) -> AuthRepo:
    """
    Создаёт и возвращает экземпляр репозитория аутентификации.

    Аргументы:
        db (AsyncSession): Асинхронная сессия базы данных.

    Возвращает:
        AuthRepo: Репозиторий аутентификации с доступом к базе данных.
    """
    return AuthRepo(db)
