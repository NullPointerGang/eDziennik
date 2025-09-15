from typing import List
from sqlalchemy import Integer, String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from core.database import Base
from core.database.schemas.user_roles import user_roles 

class Roles(Base):
    __tablename__ = 'roles'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250))
    users: Mapped[List["User"]] = relationship(
        "User",
        secondary=user_roles,
        back_populates="roles",
        lazy="selectin",
    )
