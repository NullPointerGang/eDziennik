from app.user.schemas.user_schem import User
from app.user.schemas.role_schem import Roles
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from core.security.password import verify_password, get_password_hash
from core.exceptions.auth import UserNotFound


class AuthRepo:
    def __init__(self, db: AsyncSession):
        self.db: AsyncSession = db

    async def verify_user(self, email: str, password: str) -> User:
        """
        Проверяет, существует ли пользователь в системе.

        Возвращает:
            User: Схема пользователя (app.auth.schemas.user_schem.User) при успешном поиске.

        Вызывает:
            UserNotFound: Исключение (core.exceptions.auth.UserNotFound) если пользователь с указанными данными не найден.
        """

        query = (
            select(User)
            .options(selectinload(User.roles))
            .where(User.email == email)
        )
        result = await self.db.execute(query)
        user: User = result.scalars().first()
        if user and verify_password(password, user.hased_password):
            return user
            
        raise UserNotFound
        
    async def get_user_by_email(self, user_email: str) -> User:
        """

        Возвращает:
           User: модель пользователя

        Вызывает:
            UserNotFound: Исключение (core.exceptions.auth.UserNotFound) если пользователь с указанными данными не найден.
        """

        query = (
            select(User)
            .options(selectinload(User.roles))
            .where(User.email == user_email)
        )
        result = await self.db.execute(query)
        user: User = result.scalars().first()

        if user is not None:
            return user
        else:
            raise UserNotFound

    async def get_user_by_id(self, user_id: int) -> User:
        """
        Получает пользователя по его ID.

        Аргументы:
            user_id (int): ID пользователя.

        Возвращает:
            User: модель пользователя.

        Вызывает:
            UserNotFound: Исключение (core.exceptions.auth.UserNotFound) если пользователь с указанным ID не найден.
        """

        query = (
            select(User)
            .options(selectinload(User.roles))
            .where(User.id == user_id)
        )
        result = await self.db.execute(query)
        user: User = result.scalars().first()

        if user is not None:
            return user
        else:
            raise UserNotFound
        
    async def create_user(self, email: str, first_name: str, last_name: str, password: str, role_name: str | None = None) -> User:
        """
        Создаёт нового пользователя в базе данных.

        Аргументы:
            email (str): электронная почта пользователя.
            first_name (str): имя пользователя.
            last_name (str): фамилия пользователя.
            hashed_password (str): уже захешированный пароль.

        Возвращает:
            User: созданная модель пользователя.
        """

        new_user = User(
            email=email,
            first_name=first_name,
            last_name=last_name,
            hased_password=get_password_hash(password)
        )
        if role_name:
            result = await self.db.execute(select(Roles).where(Roles.name == role_name))
            role = result.scalars().first()
            if role is not None:
                new_user.roles.append(role)
        self.db.add(new_user)
        await self.db.commit()
        await self.db.refresh(new_user)
        return new_user