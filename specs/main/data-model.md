# Data Model: Phase III Todo AI Chatbot

**Date**: 2026-02-05 | **Database**: Neon PostgreSQL

## Entity Relationship Diagram

```
┌─────────────────────┐       ┌─────────────────────┐
│       tasks         │       │   conversations     │
├─────────────────────┤       ├─────────────────────┤
│ id (PK)             │       │ id (PK, UUID)       │
│ title               │       │ user_id (IDX)       │
│ description         │       │ title               │
│ completed           │       │ created_at          │
│ priority            │       │ updated_at          │
│ due_date            │       └──────────┬──────────┘
│ user_id (IDX)       │                  │
│ created_at          │                  │ 1:N
│ updated_at          │                  │
└─────────────────────┘       ┌──────────▼──────────┐
                              │     messages        │
                              ├─────────────────────┤
                              │ id (PK)             │
                              │ conversation_id (FK)│
                              │ role                │
                              │ content             │
                              │ tool_calls (JSON)   │
                              │ created_at          │
                              └─────────────────────┘
```

## Entities

### Task

Represents a todo item managed by the user via AI chatbot.

```python
from datetime import datetime
from sqlmodel import SQLModel, Field

class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(max_length=255, index=True)
    description: str | None = Field(default=None, max_length=2000)
    completed: bool = Field(default=False)
    priority: str = Field(default="medium")  # Enum: low, medium, high
    due_date: datetime | None = Field(default=None)
    user_id: str = Field(max_length=100, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

**Validation Rules**:
- `title`: Required, 1-255 characters
- `priority`: Must be one of: "low", "medium", "high"
- `user_id`: Required, identifies task owner

**Indexes**:
- `user_id`: For filtering tasks by user
- `title`: For text search

### Conversation

Represents a chat session between user and AI.

```python
from datetime import datetime
from sqlmodel import SQLModel, Field
import uuid

class Conversation(SQLModel, table=True):
    __tablename__ = "conversations"

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    user_id: str = Field(max_length=100, index=True)
    title: str | None = Field(default=None, max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

**Validation Rules**:
- `id`: Auto-generated UUID
- `user_id`: Required, identifies conversation owner
- `title`: Optional, auto-generated from first message

**Indexes**:
- `user_id`: For listing user's conversations

### Message

Represents a single message in a conversation.

```python
from datetime import datetime
from sqlmodel import SQLModel, Field

class Message(SQLModel, table=True):
    __tablename__ = "messages"

    id: int | None = Field(default=None, primary_key=True)
    conversation_id: str = Field(foreign_key="conversations.id", index=True)
    role: str = Field(max_length=20)  # Enum: user, assistant, tool
    content: str = Field()
    tool_calls: str | None = Field(default=None)  # JSON serialized
    created_at: datetime = Field(default_factory=datetime.utcnow)
```

**Validation Rules**:
- `conversation_id`: Required, must reference valid conversation
- `role`: Must be one of: "user", "assistant", "tool"
- `content`: Required, message text

**Indexes**:
- `conversation_id`: For loading conversation history

## State Transitions

### Task States

```
[Created] ──complete_task──> [Completed]
    │                            │
    └──────delete_task───────────┴──> [Deleted]
```

### Conversation Lifecycle

```
[New] ──first message──> [Active] ──delete──> [Deleted]
```

## Database Migrations

Initial migration creates all tables:

```sql
-- Create tasks table
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    completed BOOLEAN DEFAULT FALSE,
    priority VARCHAR(20) DEFAULT 'medium',
    due_date TIMESTAMP,
    user_id VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_title ON tasks(title);

-- Create conversations table
CREATE TABLE conversations (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(100) NOT NULL,
    title VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_conversations_user_id ON conversations(user_id);

-- Create messages table
CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    conversation_id VARCHAR(36) NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
    role VARCHAR(20) NOT NULL,
    content TEXT NOT NULL,
    tool_calls TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_messages_conversation_id ON messages(conversation_id);
```
