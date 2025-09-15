from dotenv import load_dotenv

load_dotenv()

import os
import yaml
import base64
from functools import lru_cache
from pydantic import BaseModel
from typing import List, Literal


class AppConfig(BaseModel):
    title: str = "eDziennik"
    version: str = "0.0.1"
    logo_url: str = ""

class UvicornConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000
    workers: int = 4

class CORSConfig(BaseModel):
    allow_origins: List[str] = ["*"]
    allow_credentials: bool = True
    allow_methods: List[str] = ["*"]
    allow_headers: List[str] = ["*"]
    expose_headers: List[str] = ["*"]

class JWTConfig(BaseModel):
    secret_key: str = os.getenv("SECRET_KEY", "")
    algorithm: str = "HS256"
    default_max_age_in_minutes: int = 60 * 60 * 24 * 3
    remember_me_max_age_in_minutes: int = 60 * 60 * 24 * 30

class LoggingConfig(BaseModel):
    level: int = 20
    format: str = "%(asctime)s - %(levelname)s - %(message)s"
    logs_dir: str = "./logs"
    dev_mode: bool = False
    log_to_console: bool = True
    ignore_endpoints: List[str] = ["/api/docs", "/api/redoc", "/api/openapi.json"]

class DatabaseConfig(BaseModel):
    connect_string: str = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./test.db")

class CookiesSettings(BaseModel):
    secure: bool = True
    httponly: bool = True
    samesite: Literal["lax", "strict", "none"] | None = "lax"
    domain: str | None = os.getenv("DOMAIN")

class Config(BaseModel):
    app: AppConfig = AppConfig()
    uvicorn: UvicornConfig = UvicornConfig()
    cors: CORSConfig = CORSConfig()
    jwt: JWTConfig = JWTConfig()
    logging: LoggingConfig = LoggingConfig()
    database: DatabaseConfig = DatabaseConfig()
    cookies: CookiesSettings = CookiesSettings()


class LoadConfig:
    def load_config(self, config_path: str = "./config.yaml") -> Config:
        """
        Загружает конфигурацию из YAML файла.

        Аргументы:
            config_path (str, optional): Путь к файлу конфигурации YAML. По умолчанию "./config.yaml".

        Возвращает:
            Config: Объект конфигурации, заполненный из файла.
        """
        with open(config_path, "r") as file:
            yaml_config = yaml.safe_load(file) or {}
        
        return Config(**yaml_config)

    @lru_cache
    def get_config(self) -> Config:
        """
        Возвращает кешированную конфигурацию приложения.

        Если переменная окружения CONFIG_PATH установлена,
        загружает конфигурацию из указанного файла, иначе — из "config.yaml".

        Возвращает:
            Config: Объект конфигурации приложения.
        """
        config_path = os.getenv("CONFIG_PATH")
        if config_path:
            return self.load_config(config_path)
        else:
            return self.load_config("config.yaml")
