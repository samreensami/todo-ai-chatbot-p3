"""Dashboard API router for tasks management - FIXED VERSION."""
from datetime import datetime, timedelta
from typing import Optional, List
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db_session
from app.models import Task

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

# --- Response Schemas ---
class TaskRead(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    status: bool  # Frontend uses 'status'
    priority: str = "medium"
    due_date: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class DashboardStats(BaseModel):
    tasksCompleted: int
    pendingTasks: int
    upcomingDeadlines: int

# --- Helper Function ---
def task_to_response(task: Task) -> TaskRead:
    return TaskRead(
        id=task.id,
        title=task.title,
        description=task.description,
        status=task.completed,
        priority=task.priority,
        due_date=task.due_date,
        created_at=task.created_at,
        updated_at=task.updated_at,
    )

# --- Routes ---

@router.get("/stats", response_model=DashboardStats)
async def get_dashboard_stats():
    async with get_db_session() as session:
        # Completed
        res_comp = await session.execute(select(Task).where(Task.completed == True))
        completed_count = len(res_comp.scalars().all())

        # Pending
        res_pend = await session.execute(select(Task).where(Task.completed == False))
        pending_count = len(res_pend.scalars().all())

        # Upcoming
        now = datetime.utcnow()
        week_limit = now + timedelta(days=7)
        res_up = await session.execute(
            select(Task).where(Task.due_date <= week_limit, Task.completed == False)
        )
        upcoming_count = len(res_up.scalars().all())

        return DashboardStats(
            tasksCompleted=completed_count,
            pendingTasks=pending_count,
            upcomingDeadlines=upcoming_count
        )

@router.get("/tasks", response_model=List[TaskRead])  # FIXED: Removed trailing slash
async def list_tasks():
    async with get_db_session() as session:
        query = select(Task).order_by(Task.created_at.desc())
        result = await session.execute(query)
        tasks = result.scalars().all()
        return [task_to_response(task) for task in tasks]

@router.post("/tasks", response_model=TaskRead)  # FIXED: Removed trailing slash
async def create_task(task_data: dict): # Using dict for flexibility
    async with get_db_session() as session:
        new_task = Task(
            title=task_data.get("title"),
            description=task_data.get("description"),
            completed=task_data.get("status", False),
            priority=task_data.get("priority", "medium"),
            user_id="demo-user"
        )
        session.add(new_task)
        await session.commit()
        await session.refresh(new_task)
        return task_to_response(new_task)

@router.put("/tasks/{task_id}", response_model=TaskRead)
async def update_task(task_id: int, task_data: dict):
    async with get_db_session() as session:
        task = await session.get(Task, task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")

        # Update fields if provided
        if "title" in task_data:
            task.title = task_data["title"]
        if "description" in task_data:
            task.description = task_data["description"]
        if "status" in task_data:
            task.completed = task_data["status"]
        if "priority" in task_data:
            task.priority = task_data["priority"]
        if "due_date" in task_data:
            task.due_date = task_data["due_date"]

        task.updated_at = datetime.utcnow()
        await session.commit()
        await session.refresh(task)
        return task_to_response(task)

@router.delete("/tasks/{task_id}")
async def delete_task(task_id: int):
    async with get_db_session() as session:
        task = await session.get(Task, task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        await session.delete(task)
        await session.commit()
        return {"success": True}