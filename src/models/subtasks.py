import sqlalchemy as sa
from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.model_base import ModelBase

class SubTask(ModelBase):
    __tablename__ = 'subtask'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    description: Mapped[str] = mapped_column(sa.String(250))
    registration_date: Mapped[datetime] = mapped_column(sa.DateTime, default=sa.func.now())
    due_date: Mapped[Optional[sa.Date]] = mapped_column(sa.Date)
    status: Mapped[bool] = mapped_column(sa.Boolean, default=False)
    
    group_task_id: Mapped[int] = mapped_column(
        sa.ForeignKey('task.id', ondelete='CASCADE'), 
        index=True
    )
    task: Mapped["Task"] = relationship("Task", back_populates="subtasks")

    def __repr__(self):
        return f"<SubTask(description={self.description})>"