from app.auth.repositories import auth_repo
from app.auth.models.auth_model import LoginRequest, RegisterRequest
from core.security.jwt import JWTManager
from core.exceptions.auth import UserNotFound
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from core.config import config
from core.logging import logger
from app.user.schemas.user_schem import User


class AuthService:
    def __init__(self, auth_repo: auth_repo.AuthRepo):
        """
        Инициализирует сервис аутентификации.

        Аргументы:
            auth_repo (AuthRepo): Репозиторий для работы с пользователями и MFA.
        """
        self.auth_repo = auth_repo
        self.jwt_manager = JWTManager()

    async def login(self, login_request: LoginRequest, remember_me: bool = False) -> JSONResponse:
        """
        Выполняет вход пользователя по email и паролю.

        Если у пользователя включена двухфакторная аутентификация, возвращает временный токен
        для прохождения MFA.

        Аргументы:
            login_request (LoginRequest): Данные для входа (email и пароль).
            remember_me (bool): Флаг "запомнить меня" для увеличенного срока жизни токена.

        Возвращает:
            JSONResponse: Ответ с JWT токеном и флагом необходимости MFA.

        Вызывает:
            HTTPException: В случае внутренних ошибок сервера.
        """
        try:
            user: User = await self.auth_repo.verify_user(login_request.email, login_request.password)
        except UserNotFound:
            logger.error(f"User {login_request.email} not found")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={
                    "detail": "Invalid credentials"
                },
            )
        except Exception as e:
            logger.error(f"Error when attempting to log in as user {login_request.email}. Error: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Something went wrong",
            )

        access_token = self.jwt_manager.create_token(
            {"sub": user.email, "user_id": user.id},
            remember_me=remember_me
        )
        role_names = [r.name for r in (user.roles or [])]
        response = JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "access_token": access_token,
                "token_type": "bearer",
                "roles": role_names,
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "roles": role_names
                }
            }
        )
        response.set_cookie(
            key="access_token",
            value=f"Bearer {access_token}",
            max_age=config.jwt.remember_me_max_age_in_minutes if remember_me else config.jwt.default_max_age_in_minutes,
            path="/",
            domain=config.cookies.domain,
            secure=config.cookies.secure,
            httponly=True,
            samesite=config.cookies.samesite,
        )
        return response

        
    async def logout(self) -> JSONResponse:
        """
        Выполняет выход пользователя, удаляя cookies с токенами доступа.

        Возвращает:
            JSONResponse: Ответ с подтверждением выхода.
        """
        response = JSONResponse(
            {
                "message": "Logged out"
            },
            status_code=status.HTTP_200_OK,
        )
        response.delete_cookie("access_token")
        return response

    async def register(self, register_request: RegisterRequest) -> JSONResponse:
        # Проверяем существование пользователя с таким email
        try:
            await self.auth_repo.get_user_by_email(register_request.email)
            # Если не выброшено исключение, пользователь уже существует
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={"detail": "User with this email already exists"}
            )
        except UserNotFound:
            pass

        user = await self.auth_repo.create_user(
            register_request.email, 
            register_request.first_name, 
            register_request.last_name, 
            register_request.password,
            role_name=register_request.role
        )
        if user:
            return await self.login(LoginRequest(
                email=register_request.email,
                password=register_request.password
            ))
        else: 
            raise HTTPException(
                status_code=500 
            )
        
