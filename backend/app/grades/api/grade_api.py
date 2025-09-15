from typing import Annotated, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from app.grades.dependencies.get_grade_service import get_grade_service
from app.grades.services.grade_service import GradeService
from app.grades.models.grade_model import GradeCreate, GradeUpdate, GradeResponse


router = APIRouter(prefix="/grades", tags=["grades"])


@router.get("/", response_model=List[GradeResponse], status_code=status.HTTP_200_OK)
async def list_grades(
    service: Annotated[GradeService, Depends(get_grade_service)],
    student_id: Optional[int] = Query(default=None)
):
    grades = await service.list_grades(student_id)
    return [GradeResponse(**g.__dict__) for g in grades]


@router.get("/{grade_id}", response_model=GradeResponse, status_code=status.HTTP_200_OK)
async def get_grade(grade_id: int, service: Annotated[GradeService, Depends(get_grade_service)]):
    g = await service.get_grade(grade_id)
    if not g:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Grade not found")
    return GradeResponse(**g.__dict__)


@router.post("/", response_model=GradeResponse, status_code=status.HTTP_201_CREATED)
async def create_grade(payload: GradeCreate, service: Annotated[GradeService, Depends(get_grade_service)]):
    g = await service.create_grade(payload.dict())
    return GradeResponse(**g.__dict__)


@router.patch("/{grade_id}", response_model=GradeResponse, status_code=status.HTTP_200_OK)
async def update_grade(grade_id: int, payload: GradeUpdate, service: Annotated[GradeService, Depends(get_grade_service)]):
    g = await service.update_grade(grade_id, {k: v for k, v in payload.dict().items() if v is not None})
    if not g:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Grade not found")
    return GradeResponse(**g.__dict__)


@router.delete("/{grade_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_grade(grade_id: int, service: Annotated[GradeService, Depends(get_grade_service)]):
    await service.delete_grade(grade_id)
    return None


