from app.auth.services.auth_service import AuthService
from app.auth.dependencies.get_auth_repo import get_auth_repo
from fastapi import Depends
from app.auth.repositories.auth_repo import AuthRepo


def get_auth_service(auth_repo: AuthRepo = Depends(get_auth_repo)) -> AuthService:
    """
    Создаёт и возвращает экземпляр сервиса аутентификации.

    Аргументы:
        auth_repo (AuthRepo): Репозиторий аутентификации.

    Возвращает:
        AuthService: Сервис аутентификации для бизнес-логики.
    """
    return AuthService(auth_repo)
