import os
import pyotp
import base64
import secrets
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from core.config import config


class TOTPManager:
    def _encrypt_secret(self, secret: str) -> bytes:
        """
        Шифрует секрет TOTP с помощью AES-GCM.

        Аргументы:
            secret (str): Открытый секрет TOTP.

        Возвращает:
            bytes: Зашифрованные данные (nonce + ciphertext).
        """
        aesgcm = AESGCM(config.totp.encryption_key)
        nonce = os.urandom(12)
        ciphertext = aesgcm.encrypt(nonce, secret.encode(), None)
        return nonce + ciphertext

    def _decrypt_secret(self, encrypted_data: bytes) -> str:
        """
        Расшифровывает секрет TOTP из зашифрованных данных.

        Аргументы:
            encrypted_data (bytes): Зашифрованные данные (nonce + ciphertext).

        Возвращает:
            str: Открытый секрет TOTP.
        """
        aesgcm = AESGCM(config.totp.encryption_key)
        nonce = encrypted_data[:12]
        ciphertext = encrypted_data[12:]
        return aesgcm.decrypt(nonce, ciphertext, None).decode()

    def create_totp(self, secret: str) -> pyotp.TOTP:
        """
        Создаёт объект TOTP на основе секрета.

        Аргументы:
            secret (str): Открытый секрет TOTP.

        Возвращает:
            pyotp.TOTP: Объект TOTP.
        """
        return pyotp.TOTP(secret, digits=config.totp.digits, interval=config.totp.period)

    def check_totp_code(self, totp_code: str, encrypted_secret: bytes) -> bool:
        """
        Проверяет корректность TOTP-кода.

        Аргументы:
            totp_code (str): Код, введённый пользователем.
            encrypted_secret (bytes): Зашифрованный секрет TOTP.

        Возвращает:
            bool: True, если код корректен, иначе False.
        """
        secret = self._decrypt_secret(encrypted_secret)
        totp = self.create_totp(secret)
        return totp.verify(totp_code)

    def create_totp_secret(self) -> tuple[str, bytes]:
        """
        Генерирует новый секрет TOTP и возвращает его в открытом и зашифрованном виде.

        Возвращает:
            tuple[str, bytes]: Кортеж из открытого секрета (base32) и зашифрованного секрета.
        """
        secret_bytes = secrets.token_bytes(config.totp.secret_len)
        secret = base64.b32encode(secret_bytes).decode('utf-8').rstrip('=')
        encrypted_secret = self._encrypt_secret(secret)
        return secret, encrypted_secret

    def get_totp_uri(self, encrypted_secret: bytes, email: str, issuer_name: str = config.totp.issuer_name) -> str:
        """
        Формирует URI для настройки TOTP в приложениях-аутентификаторах.

        Аргументы:
            encrypted_secret (bytes): Зашифрованный секрет TOTP.
            email (str): Email пользователя, используется в URI.
            issuer_name (str, optional): Имя издателя (по умолчанию из конфига).

        Возвращает:
            str: URI для настройки TOTP.
        """
        secret = self._decrypt_secret(encrypted_secret)
        return pyotp.TOTP(secret).provisioning_uri(
            name=email, 
            issuer_name=issuer_name
        )
    
totp_manager = TOTPManager()

