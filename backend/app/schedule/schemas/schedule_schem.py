from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from core.database import Base


class ScheduleItem(Base):
    __tablename__ = 'schedule'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    class_name: Mapped[str] = mapped_column(String(50), nullable=False)
    weekday: Mapped[int] = mapped_column(Integer, nullable=False)  # 1..7
    time_from: Mapped[str] = mapped_column(String(10), nullable=False)  # HH:MM
    time_to: Mapped[str] = mapped_column(String(10), nullable=False)    # HH:MM
    subject: Mapped[str] = mapped_column(String(100), nullable=False)
    teacher_id: Mapped[int] = mapped_column(Integer, nullable=True)


