# Tool Calling Logic Documentation

## Overview
The `tools.py` file contains the core functions that enable AI agents to interact with the task management system. These functions serve as the bridge between the AI model's understanding of user requests and the actual database operations.

## Functions

### `add_task(session, user_id, title, description=None, category=None)`
- Purpose: Creates a new task in the database
- Parameters:
  - `session`: Database session for SQLModel operations
  - `user_id`: ID of the user creating the task
  - `title`: Title of the task (required)
  - `description`: Optional description of the task
  - `category`: Optional category for organizing tasks
- Returns: Dictionary representation of the created task

### `list_tasks(session, user_id, status=None)`
- Purpose: Retrieves tasks for a specific user, optionally filtered by status
- Parameters:
  - `session`: Database session for SQLModel operations
  - `user_id`: ID of the user whose tasks to retrieve
  - `status`: Optional filter ('all', 'pending', 'completed')
- Returns: List of dictionary representations of tasks

### `complete_task(session, user_id, task_id)`
- Purpose: Marks a specific task as completed
- Parameters:
  - `session`: Database session for SQLModel operations
  - `user_id`: ID of the user who owns the task
  - `task_id`: ID of the task to mark as completed
- Returns: Dictionary with task_id, status, and title of the completed task

### `delete_task(session, user_id, task_id)`
- Purpose: Removes a specific task from the database
- Parameters:
  - `session`: Database session for SQLModel operations
  - `user_id`: ID of the user who owns the task
  - `task_id`: ID of the task to delete
- Returns: Dictionary with task_id, status, and title of the deleted task

### `update_task(session, user_id, task_id, title=None, description=None, category=None, status=None)`
- Purpose: Updates properties of an existing task
- Parameters:
  - `session`: Database session for SQLModel operations
  - `user_id`: ID of the user who owns the task
  - `task_id`: ID of the task to update
  - `title`: New title (optional)
  - `description`: New description (optional)
  - `category`: New category (optional)
  - `status`: New status (optional)
- Returns: Dictionary representation of the updated task

## Implementation Notes
- All functions follow a consistent pattern of accepting a database session and user_id
- Error handling is implemented where appropriate (e.g., checking if tasks exist)
- The functions return standardized dictionary representations of tasks
- These functions are called by the AI agent through the tool mapping in chat.py