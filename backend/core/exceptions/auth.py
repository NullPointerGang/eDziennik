class AuthBaseException(Exception):
    """
    Базовое исключение для ошибок авторизации/аутентификации.
    """
    pass


class UserNotFound(AuthBaseException):
    """
    Пользователь не найден.
    """
    pass


class InvalidCredentials(AuthBaseException):
    """
    Неверный логин или пароль.
    """
    pass


class TokenExpired(AuthBaseException):
    """
    Срок действия токена истёк.
    """
    pass


class TokenInvalid(AuthBaseException):
    """
    Токен недействителен или повреждён.
    """
    pass


class PermissionDenied(AuthBaseException):
    """
    Недостаточно прав для выполнения операции.
    """
    pass


class AccountLocked(AuthBaseException):
    """
    Аккаунт заблокирован администратором или системой.
    """
    pass


"""
MFA (многофакторная аутентификация)
"""

class MFARequired(AuthBaseException):
    """
    Для входа требуется многофакторная аутентификация.
    """
    pass


class MFAFailed(AuthBaseException):
    """
    Не удалось пройти многофакторную аутентификацию.
    """
    pass
