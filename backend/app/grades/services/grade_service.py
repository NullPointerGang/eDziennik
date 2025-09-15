from typing import List, Optional
from app.grades.repositories.grade_repo import GradeRepo
from app.grades.schemas.grade_schem import Grade


class GradeService:
    def __init__(self, repo: GradeRepo):
        self.repo = repo

    async def list_grades(self, student_id: Optional[int] = None) -> List[Grade]:
        return await self.repo.list_grades(student_id)

    async def get_grade(self, grade_id: int) -> Optional[Grade]:
        return await self.repo.get_grade(grade_id)

    async def create_grade(self, payload: dict) -> Grade:
        return await self.repo.create_grade(payload)

    async def update_grade(self, grade_id: int, payload: dict) -> Optional[Grade]:
        return await self.repo.update_grade(grade_id, payload)

    async def delete_grade(self, grade_id: int) -> None:
        await self.repo.delete_grade(grade_id)


