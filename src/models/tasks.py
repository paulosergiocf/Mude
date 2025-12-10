import sqlalchemy as sa
from typing import List, Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.model_base import ModelBase

class Task(ModelBase):
    __tablename__ = 'task'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(sa.String(250))
    description: Mapped[Optional[str]] = mapped_column(sa.Text)
    start_date: Mapped[Optional[sa.Date]] = mapped_column(sa.Date)
    end_date: Mapped[Optional[sa.Date]] = mapped_column(sa.Date, nullable=True)
    status: Mapped[bool] = mapped_column(sa.Boolean, default=True)
    
    subtasks: Mapped[List["SubTask"]] = relationship(
        "SubTask", 
        back_populates="task", 
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Task(name={self.name!r})>"