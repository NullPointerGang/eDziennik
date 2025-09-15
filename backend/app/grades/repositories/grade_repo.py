from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete
from app.grades.schemas.grade_schem import Grade


class GradeRepo:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_grades(self, student_id: Optional[int] = None) -> List[Grade]:
        stmt = select(Grade)
        if student_id is not None:
            stmt = stmt.where(Grade.student_id == student_id)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_grade(self, grade_id: int) -> Optional[Grade]:
        result = await self.db.execute(select(Grade).where(Grade.id == grade_id))
        return result.scalars().first()

    async def create_grade(self, payload: dict) -> Grade:
        grade = Grade(**payload)
        self.db.add(grade)
        await self.db.commit()
        await self.db.refresh(grade)
        return grade

    async def update_grade(self, grade_id: int, payload: dict) -> Optional[Grade]:
        await self.db.execute(
            update(Grade)
            .where(Grade.id == grade_id)
            .values(**payload)
        )
        await self.db.commit()
        return await self.get_grade(grade_id)

    async def delete_grade(self, grade_id: int) -> None:
        await self.db.execute(delete(Grade).where(Grade.id == grade_id))
        await self.db.commit()


