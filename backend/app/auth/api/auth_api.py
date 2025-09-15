from fastapi import APIRouter, Depends, Request, Query
from app.auth.models.auth_model import (
    LoginRequest, LoginResponse, RegisterRequest
)
from app.auth.services.auth_service import AuthService
from app.auth.dependencies.get_auth_service import get_auth_service


router = APIRouter(prefix="/auth")

@router.post("/login", response_model=LoginResponse, tags=["Authentication"])
async def login_route(
    login_request: LoginRequest,
    remember_me: bool = Query(False, description="Флаг 'запомнить меня' для длительной сессии"),
    service: AuthService = Depends(get_auth_service),
):
    """
    Выполняет вход пользователя по логину и паролю.

    Аргументы:
        login_request (app.auth.models.auth_model.LoginRequest): Данные для входа (логин и пароль).
        remember_me (bool, optional): Флаг "запомнить меня" для длительной сессии.
        service (app.auth.services.auth_service.AuthService): Сервис аутентификации.

    Возвращает:
        JSONResponse: Ответ с информацией о сессии пользователя и токенами.
    """
    return await service.login(login_request, remember_me)

@router.post("/logout", tags=["Authentication"])
async def logout_route(
    service: AuthService = Depends(get_auth_service)
):
    """
    Выполняет выход пользователя из системы.

    Аргументы:
        service (app.auth.services.auth_service.AuthService): Сервис аутентификации.

    Возвращает:
        JSONResponse: Результат успешного выхода (например, сообщение или статус).
    """
    return await service.logout()

@router.post("/register", tags=["Authentication"])
async def register_route(
    register_request: RegisterRequest,
    service: AuthService = Depends(get_auth_service)
):
    return await service.register(register_request)
    