import secrets
import hashlib
from typing import List


class RecoveryCodeManager:
    def generate_recovery_codes(self, count: int = 10) -> List[str]:
        """
        Генерирует список кодов восстановления.

        Аргументы:
            count (int, optional): Количество кодов для генерации. По умолчанию 10.

        Возвращает:
            List[str]: Список сгенерированных кодов восстановления.
        """
        codes = []
        for _ in range(count):
            code = secrets.token_hex(3)
            codes.append(code)
        return codes
    
    def verify_recovery_code(self, code: str, code_hash: str) -> bool:
        """
        Проверяет, совпадает ли хэш кода восстановления с переданным хэшем.

        Аргументы:
            code (str): Код восстановления в открытом виде.
            code_hash (str): Хэш кода восстановления.

        Возвращает:
            bool: True, если код совпадает с хэшем, иначе False.
        """
        return hashlib.sha256(code.encode()).hexdigest() == code_hash
    
    def hash_recovery_code(self, code: str) -> str:
        """
        Вычисляет SHA256-хэш для кода восстановления.

        Аргументы:
            code (str): Код восстановления в открытом виде.

        Возвращает:
            str: Хэш кода восстановления.
        """
        return hashlib.sha256(code.encode()).hexdigest()

recovery_code_manager = RecoveryCodeManager()

