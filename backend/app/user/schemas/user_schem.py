from typing import List
from sqlalchemy import Integer, String, ForeignKey, LargeBinary
from sqlalchemy.orm import relationship, Mapped, mapped_column
from core.database import Base
from core.database.schemas.user_roles import user_roles

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    hased_password: Mapped[bytes] = mapped_column(LargeBinary(128), nullable=False)

    roles: Mapped[List["Roles"]] = relationship(
        "Roles",
        secondary=user_roles,
        back_populates="users",
        lazy="selectin",
    )