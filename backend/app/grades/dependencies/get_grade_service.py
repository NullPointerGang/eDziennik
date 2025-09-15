from typing import Annotated
from fastapi import Depends
from app.grades.services.grade_service import GradeService
from app.grades.repositories.grade_repo import GradeRepo
from app.grades.dependencies.get_grade_repo import get_grade_repo


async def get_grade_service(repo: Annotated[GradeRepo, Depends(get_grade_repo)]) -> GradeService:
    return GradeService(repo)


