from pydantic import BaseModel, EmailStr
from typing import List, Literal


class LoginRequest(BaseModel):
    """
    Модель запроса для входа пользователя.

    Атрибуты:
        email (EmailStr): Email пользователя.
        password (str): Пароль пользователя.
    """
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    """
    Модель ответа после успешного входа.

    Атрибуты:
        access_token (str): Токен доступа для авторизации.
        token_type (str): Тип токена (например, "bearer").
    """
    access_token: str
    token_type: str


class RegisterRequest(BaseModel):
    """
    Модель запроса для регистрации пользователя.

    Атрибуты:
        email (EmailStr): Email пользователя.
        password (str): Пароль пользователя.
    """

    email: EmailStr
    password: str
    first_name: str
    last_name: str
    role: Literal["student", "teacher"]