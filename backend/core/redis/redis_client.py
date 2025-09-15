from __future__ import annotations
import asyncio
from typing import Optional, AsyncGenerator
from redis.asyncio import Redis, ConnectionPool
from core.config import config


class AsyncRedisClient:
    _pool: Optional[ConnectionPool] = None
    _client: Optional[Redis] = None
    _lock: asyncio.Lock = asyncio.Lock()

    @classmethod
    def _build_url(cls) -> str:
        cfg = config.redis
        if getattr(cfg, "url", None):
            return cfg.url # type: ignore
        scheme = "rediss" if cfg.ssl else "redis"
        auth_part = ""
        if cfg.username and cfg.password:
            auth_part = f"{cfg.username}:{cfg.password}@"
        elif cfg.password:
            auth_part = f":{cfg.password}@"
        host_part = f"{cfg.host}:{cfg.port}"
        db_part = f"/{cfg.db}"
        return f"{scheme}://{auth_part}{host_part}{db_part}"

    @classmethod
    async def get_client(cls) -> Redis:
        if cls._client is not None:
            return cls._client
        async with cls._lock:
            if cls._client is None:
                url = cls._build_url()
                cls._pool = ConnectionPool.from_url(
                    url,
                    max_connections=config.redis.max_connections,
                    socket_timeout=config.redis.socket_timeout,
                    decode_responses=True,
                    retry_on_timeout=True,
                )
                cls._client = Redis(connection_pool=cls._pool)
        return cls._client # type: ignore

    @classmethod
    async def close(cls) -> None:
        if cls._client is not None:
            try:
                await cls._client.close()
            finally:
                try:
                    await cls._client.connection_pool.disconnect()  # type: ignore
                except Exception:
                    pass
            cls._client = None
        if cls._pool is not None:
            try:
                await cls._pool.disconnect()
            except Exception:
                pass
            cls._pool = None


async def get_redis() -> AsyncGenerator[Redis, None]:
    client = await AsyncRedisClient.get_client()
    try:
        yield client
    finally:
        pass

