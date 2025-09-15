from typing import Annotated
from fastapi import Depends, Header, HTTPException, status
from app.auth.dependencies.get_jwt_decode_service import get_jwt_decode_service
from app.auth.services.jwt_decode_service import JWTDecodeService


async def get_current_user_id(
    authorization: str | None = Header(default=None),
    decoder: Annotated[JWTDecodeService, Depends(get_jwt_decode_service)] = None,
) -> int:
    if not authorization:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing Authorization header")
    token = authorization.replace("Bearer ", "").strip()
    data = await decoder.decode_token(token)
    if not data.get("success"):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return int(data["user_id"]) 


