from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db
from app.grades.repositories.grade_repo import GradeRepo


async def get_grade_repo(db: Annotated[AsyncSession, Depends(get_db)]) -> GradeRepo:
    return GradeRepo(db)


