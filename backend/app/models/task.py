from datetime import datetime
from sqlmodel import SQLModel, Field
from typing import Optional


class TaskBase(SQLModel):
    """Base task model with shared fields."""
    title: str = Field(max_length=255, index=True)
    description: Optional[str] = Field(default=None, max_length=2000)
    completed: bool = Field(default=False)
    priority: str = Field(default="medium")  # low, medium, high
    due_date: Optional[datetime] = Field(default=None)
    user_id: str = Field(max_length=100, index=True)


class Task(TaskBase, table=True):
    """Task database model."""
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class TaskCreate(SQLModel):
    """Schema for creating a task."""
    title: str
    description: Optional[str] = None
    priority: str = "medium"
    due_date: Optional[datetime] = None
    user_id: str = "default"


class TaskUpdate(SQLModel):
    """Schema for updating a task."""
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[str] = None
    due_date: Optional[datetime] = None
    completed: Optional[bool] = None


class TaskResponse(TaskBase):
    """Schema for task response."""
    id: int
    created_at: datetime
    updated_at: datetime
