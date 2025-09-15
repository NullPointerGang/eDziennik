from typing import Annotated
from fastapi import Depends
from app.auth.services.jwt_decode_service import JWTDecodeService
from app.auth.dependencies.get_auth_repo import get_auth_repo
from app.auth.repositories.auth_repo import AuthRepo


async def get_jwt_decode_service(repo: Annotated[AuthRepo, Depends(get_auth_repo)]) -> JWTDecodeService:
    return JWTDecodeService(repo)


