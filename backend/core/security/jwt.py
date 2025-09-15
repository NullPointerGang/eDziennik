from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional
from jose import jwt, JWTError, ExpiredSignatureError
from core.config import config
from core.exceptions.auth import TokenExpired


class JWTManager:
    def __init__(
        self,
        secret_key: str = config.jwt.secret_key,
        algorithm: str = config.jwt.algorithm,
        default_exp_minutes: int = config.jwt.default_max_age_in_minutes,
        remember_exp_minutes: int = config.jwt.remember_me_max_age_in_minutes,
    ):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.default_exp_minutes = default_exp_minutes
        self.remember_exp_minutes = remember_exp_minutes

    def create_token(
        self,
        data: Dict[str, Any],
        *,
        expires_in: Optional[int] = None,
        expire_at: Optional[datetime] = None,
        remember_me: bool = False,
    ) -> str:
        """
        Создаёт JWT токен с гибким временем жизни.
        """
        if expire_at:
            expire = expire_at
        elif expires_in is not None:
            expire = datetime.utcnow() + timedelta(minutes=expires_in)
        elif remember_me:
            expire = datetime.utcnow() + timedelta(minutes=self.remember_exp_minutes)
        else:
            expire = datetime.utcnow() + timedelta(minutes=self.default_exp_minutes)

        payload = {
            **data,
            "exp": expire,
            "iat": datetime.utcnow(),
            "remember_me": remember_me,
        }

        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    def decode_token(self, token: str) -> Dict[str, Any]:
        """
        Декодирует JWT токен и возвращает полезную нагрузку.
        """
        token = token.replace("Bearer ", "").strip()
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except ExpiredSignatureError:
            raise TokenExpired("Token has expired")
        except JWTError as e:
            raise ValueError(f"Invalid token: {e}") from e

    def is_token_alive(self, token: str) -> bool:
        """
        Проверяет, не истёк ли токен.

        Аргументы:
            token (str): JWT токен.

        Возвращает:
            bool: True, если токен жив, иначе False.

        Вызывает:
            TokenExpired: Если токен просрочен.
            ValueError: Если токен некорректен.
        """
        payload = self.decode_token(token)
        exp = payload.get("exp")
        if not exp:
            raise ValueError("Token does not contain 'exp' claim")
        
        expire_at = datetime.fromtimestamp(exp, tz=timezone.utc)
        now = datetime.now(timezone.utc)
        if expire_at < now:
            raise TokenExpired("Token has expired")

        return True
