from typing import Optional, Dict, Any
from core.security.jwt import JWTManager
from core.exceptions.auth import TokenExpired
from app.auth.repositories import auth_repo
from app.user.schemas.user_schem import User
from core.logging import logger


class JWTDecodeService:
    """
    Сервис для декодирования JWT токенов и получения информации о пользователе.
    
    Предоставляет методы для:
    - Декодирования JWT токена
    - Валидации токена
    - Получения дополнительной информации о пользователе из базы данных
    """
    
    def __init__(self, auth_repo: auth_repo.AuthRepo):
        """
        Инициализирует сервис декодирования JWT токенов.
        
        Аргументы:
            auth_repo (AuthRepo): Репозиторий для работы с пользователями.
        """
        self.auth_repo = auth_repo
        self.jwt_manager = JWTManager()

    def is_jwt_format(self, token: str) -> bool:
        if not isinstance(token, str):
            return False
        parts = token.split(".")
        return len(parts) == 3 and all(parts)


    async def decode_token(self, jwt_token: str) -> Dict[str, Any]:
        """
        Декодирует JWT токен и возвращает информацию о пользователе.
        
        Аргументы:
            jwt_token (str): JWT токен для декодирования.
            
        Возвращает:
            Dict[str, Any]: Словарь с информацией о пользователе и статусом операции.
            
        Структура ответа:
            {
                "success": bool,
                "user_id": str,
                "email": str,
                "first_name": str,
                "last_name": str,
                "two_fa_enabled": bool,
                "exp": int,
                "iat": int,
                "remember_me": bool,
                "error_message": str
            }
        """
        try:
            payload = self.jwt_manager.decode_token(jwt_token)
            
            user_id = str(payload.get("user_id", ""))
            email = payload.get("sub", "")
            exp = payload.get("exp", 0)
            iat = payload.get("iat", 0)
            remember_me = payload.get("remember_me", False)
            
            if not user_id or not email:
                logger.error(f"Invalid token payload: missing user_id or email")
                return {
                    "success": False,
                    "user_id": "",
                    "email": "",
                    "first_name": "",
                    "last_name": "",
                    "two_fa_enabled": False,
                    "exp": 0,
                    "iat": 0,
                    "remember_me": False,
                    "error_message": "Invalid token: missing required fields"
                }
            
            try:
                user: User = await self.auth_repo.get_user_by_id(int(user_id))
                
                return {
                    "success": True,
                    "user_id": user_id,
                    "email": email,
                    "first_name": user.first_name or "",
                    "last_name": user.last_name or "",
                    "two_fa_enabled": user.twoFA_enabled,
                    "exp": exp,
                    "iat": iat,
                    "remember_me": remember_me,
                    "error_message": ""
                }
                
            except Exception as e:
                logger.error(f"Error fetching user data for user_id {user_id}: {e}")
                return {
                    "success": False,
                    "user_id": user_id,
                    "email": email,
                    "first_name": "",
                    "last_name": "",
                    "two_fa_enabled": False,
                    "exp": exp,
                    "iat": iat,
                    "remember_me": remember_me,
                    "error_message": f"Token decoded successfully, but failed to fetch user data: {str(e)}"
                }
                
        except TokenExpired:
            logger.error(f"Token expired: {jwt_token[:20]}...")
            return {
                "success": False,
                "user_id": "",
                "email": "",
                "first_name": "",
                "last_name": "",
                "two_fa_enabled": False,
                "exp": 0,
                "iat": 0,
                "remember_me": False,
                "error_message": "Token has expired"
            }
            
        except (ValueError, UnicodeDecodeError) as e:
            # Игнорируем логирование ошибок невалидного формата токена
            return {
                "success": False,
                "user_id": "",
                "email": "",
                "first_name": "",
                "last_name": "",
                "two_fa_enabled": False,
                "exp": 0,
                "iat": 0,
                "remember_me": False,
                "error_message": f"Invalid token format: {str(e)}"
            }
            
        except Exception as e:
            logger.error(f"Unexpected error decoding token: {e}")
            return {
                "success": False,
                "user_id": "",
                "email": "",
                "first_name": "",
                "last_name": "",
                "two_fa_enabled": False,
                "exp": 0,
                "iat": 0,
                "remember_me": False,
                "error_message": f"Unexpected error: {str(e)}"
            }
