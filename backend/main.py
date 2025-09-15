from contextlib import asynccontextmanager
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from core.config import config
from core.logging import logger
from lynx_logger.middleware import FastAPILoggingMiddleware

from app.auth.api import auth_router
from core.database.db import init_db, seed_roles

# Ensure ORM models are imported so SQLAlchemy can configure relationships
from app.user.schemas import user_schem, role_schem  # noqa: F401



app = FastAPI(
    title=config.app.title,
    version=config.app.version,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

main_router = APIRouter(prefix="/api/v1")
main_router.include_router(auth_router)
app.include_router(main_router)

middleware_logger = logger.get_logger()
if not middleware_logger:
    raise RuntimeError("Middleware logger is not available.")

middleware = FastAPILoggingMiddleware(logger=middleware_logger)
app.middleware("http")(middleware(app))


app.add_middleware(
    CORSMiddleware,
    allow_origins=config.cors.allow_origins,
    allow_credentials=config.cors.allow_credentials,
    allow_methods=config.cors.allow_methods,
    allow_headers=config.cors.allow_headers,
    expose_headers=config.cors.expose_headers,
)


@app.on_event("startup")
async def on_startup() -> None:
    # Create tables and finalize mappers after models have been imported
    await init_db()
    await seed_roles()
