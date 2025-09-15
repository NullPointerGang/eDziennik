import bcrypt


def verify_password(plain_password: str, hashed_password: bytes) -> bool:
    """
    Проверяет совпадение обычного пароля с захешированным.

    Аргументы:
        plain_password (str): Обычный пароль пользователя.
        hashed_password (bytes): Захешированный пароль из базы данных.

    Возвращает:
        bool: True, если пароль совпадает, иначе False.
    """
    password_byte_enc = plain_password.encode("utf-8")
    return bcrypt.checkpw(password=password_byte_enc, hashed_password=hashed_password)

def get_password_hash(password: str) -> bytes:
    """
    Генерирует хеш пароля.

    Аргументы:
        password (str): Обычный пароль пользователя.

    Возвращает:
        bytes: Захешированный пароль.
    """
    password_byte_enc = password.encode("utf-8")
    return bcrypt.hashpw(password_byte_enc, bcrypt.gensalt())