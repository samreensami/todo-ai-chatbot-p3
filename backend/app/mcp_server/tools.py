"""MCP Tool implementations for task management."""
from datetime import datetime
from typing import Optional
from sqlmodel import select
from sqlalchemy import and_

from app.database import get_db_session
from app.models import Task


async def add_task(
    title: str,
    description: Optional[str] = None,
    priority: str = "medium",
    due_date: Optional[str] = None,
    user_id: str = "default"
) -> dict:
    """
    Add a new task to the todo list.

    Args:
        title: The task title (required)
        description: Optional task description
        priority: Task priority - low, medium, or high
        due_date: Optional due date in ISO format (YYYY-MM-DD)
        user_id: User identifier for multi-user support

    Returns:
        dict: Created task details with id
    """
    # Validate priority
    if priority not in ["low", "medium", "high"]:
        return {"error": f"Invalid priority: {priority}. Must be low, medium, or high."}

    # Parse due date if provided
    parsed_due_date = None
    if due_date:
        try:
            parsed_due_date = datetime.fromisoformat(due_date)
        except ValueError:
            return {"error": f"Invalid due_date format: {due_date}. Use YYYY-MM-DD."}

    async with get_db_session() as session:
        task = Task(
            title=title,
            description=description,
            priority=priority,
            due_date=parsed_due_date,
            user_id=user_id,
        )
        session.add(task)
        await session.commit()
        await session.refresh(task)

        return {
            "success": True,
            "task": {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "priority": task.priority,
                "due_date": task.due_date.isoformat() if task.due_date else None,
                "completed": task.completed,
                "created_at": task.created_at.isoformat(),
            }
        }


async def list_tasks(
    user_id: str = "default",
    completed: Optional[bool] = None,
    priority: Optional[str] = None,
    limit: int = 50
) -> dict:
    """
    List tasks with optional filters.

    Args:
        user_id: User identifier
        completed: Filter by completion status (True/False/None for all)
        priority: Filter by priority level
        limit: Maximum number of tasks to return

    Returns:
        dict: List of tasks matching criteria
    """
    async with get_db_session() as session:
        # Build query with filters
        conditions = [Task.user_id == user_id]

        if completed is not None:
            conditions.append(Task.completed == completed)

        if priority is not None:
            if priority not in ["low", "medium", "high"]:
                return {"error": f"Invalid priority: {priority}. Must be low, medium, or high."}
            conditions.append(Task.priority == priority)

        query = select(Task).where(and_(*conditions)).limit(limit).order_by(Task.created_at.desc())
        result = await session.execute(query)
        tasks = result.scalars().all()

        return {
            "success": True,
            "count": len(tasks),
            "tasks": [
                {
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "priority": task.priority,
                    "due_date": task.due_date.isoformat() if task.due_date else None,
                    "completed": task.completed,
                    "created_at": task.created_at.isoformat(),
                }
                for task in tasks
            ]
        }


async def complete_task(
    task_id: int,
    user_id: str = "default"
) -> dict:
    """
    Mark a task as completed.

    Args:
        task_id: The ID of the task to complete
        user_id: User identifier for authorization

    Returns:
        dict: Updated task details
    """
    async with get_db_session() as session:
        query = select(Task).where(and_(Task.id == task_id, Task.user_id == user_id))
        result = await session.execute(query)
        task = result.scalar_one_or_none()

        if not task:
            return {"error": f"Task with id {task_id} not found for user {user_id}."}

        task.completed = True
        task.updated_at = datetime.utcnow()
        await session.commit()
        await session.refresh(task)

        return {
            "success": True,
            "message": f"Task '{task.title}' marked as completed.",
            "task": {
                "id": task.id,
                "title": task.title,
                "completed": task.completed,
                "updated_at": task.updated_at.isoformat(),
            }
        }


async def delete_task(
    task_id: int,
    user_id: str = "default"
) -> dict:
    """
    Delete a task from the todo list.

    Args:
        task_id: The ID of the task to delete
        user_id: User identifier for authorization

    Returns:
        dict: Confirmation of deletion
    """
    async with get_db_session() as session:
        query = select(Task).where(and_(Task.id == task_id, Task.user_id == user_id))
        result = await session.execute(query)
        task = result.scalar_one_or_none()

        if not task:
            return {"error": f"Task with id {task_id} not found for user {user_id}."}

        task_title = task.title
        await session.delete(task)
        await session.commit()

        return {
            "success": True,
            "message": f"Task '{task_title}' (id: {task_id}) has been deleted.",
        }


async def update_task(
    task_id: int,
    title: Optional[str] = None,
    description: Optional[str] = None,
    priority: Optional[str] = None,
    due_date: Optional[str] = None,
    completed: Optional[bool] = None,
    user_id: str = "default"
) -> dict:
    """
    Update an existing task.

    Args:
        task_id: The ID of the task to update
        title: New title (optional)
        description: New description (optional)
        priority: New priority level (optional)
        due_date: New due date (optional)
        completed: New completion status (optional)
        user_id: User identifier for authorization

    Returns:
        dict: Updated task details
    """
    async with get_db_session() as session:
        query = select(Task).where(and_(Task.id == task_id, Task.user_id == user_id))
        result = await session.execute(query)
        task = result.scalar_one_or_none()

        if not task:
            return {"error": f"Task with id {task_id} not found for user {user_id}."}

        # Update fields if provided
        if title is not None:
            task.title = title
        if description is not None:
            task.description = description
        if priority is not None:
            if priority not in ["low", "medium", "high"]:
                return {"error": f"Invalid priority: {priority}. Must be low, medium, or high."}
            task.priority = priority
        if due_date is not None:
            try:
                task.due_date = datetime.fromisoformat(due_date)
            except ValueError:
                return {"error": f"Invalid due_date format: {due_date}. Use YYYY-MM-DD."}
        if completed is not None:
            task.completed = completed

        task.updated_at = datetime.utcnow()
        await session.commit()
        await session.refresh(task)

        return {
            "success": True,
            "message": f"Task '{task.title}' has been updated.",
            "task": {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "priority": task.priority,
                "due_date": task.due_date.isoformat() if task.due_date else None,
                "completed": task.completed,
                "updated_at": task.updated_at.isoformat(),
            }
        }
