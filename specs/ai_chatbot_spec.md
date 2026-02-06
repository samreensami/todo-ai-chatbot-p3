# Phase III: Todo AI Chatbot Specification

## Overview

A stateless AI-powered chatbot for task management, built with FastAPI, OpenAI Agents SDK, and MCP (Model Context Protocol) Server. The system persists all data to Neon PostgreSQL and provides a modern chat interface via OpenAI ChatKit UI.

## Architecture

### System Components

```
┌─────────────────────────────────────────────────────────────────┐
│                     Frontend (ChatKit UI)                        │
│                    OpenAI ChatKit Components                     │
└─────────────────────────────┬───────────────────────────────────┘
                              │ HTTP/WebSocket
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    FastAPI Backend                               │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │  Chat Endpoint  │  │  OpenAI Agents  │  │   MCP Client    │ │
│  │   /api/chat     │──│      SDK        │──│                 │ │
│  └─────────────────┘  └─────────────────┘  └────────┬────────┘ │
└─────────────────────────────────────────────────────┼───────────┘
                                                      │ MCP Protocol
                                                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                       MCP Server                                 │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                      MCP Tools                               ││
│  │  add_task │ list_tasks │ complete_task │ delete_task │      ││
│  │                     update_task                              ││
│  └─────────────────────────────────────────────────────────────┘│
└─────────────────────────────┬───────────────────────────────────┘
                              │ SQLModel ORM
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                  Neon PostgreSQL Database                        │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐ │
│  │    tasks    │  │conversations│  │      messages           │ │
│  └─────────────┘  └─────────────┘  └─────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

### Technology Stack

| Component | Technology |
|-----------|------------|
| Backend Framework | FastAPI |
| AI Integration | OpenAI Agents SDK |
| Tool Protocol | MCP (Model Context Protocol) Server |
| ORM | SQLModel |
| Database | Neon PostgreSQL (Serverless) |
| Frontend | OpenAI ChatKit UI |
| API Format | REST + Server-Sent Events (SSE) |

## Database Schema

### Tasks Table

```python
class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(max_length=255, index=True)
    description: str | None = Field(default=None)
    completed: bool = Field(default=False)
    priority: str = Field(default="medium")  # low, medium, high
    due_date: datetime | None = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    user_id: str = Field(index=True)  # For multi-user support
```

### Conversations Table

```python
class Conversation(SQLModel, table=True):
    __tablename__ = "conversations"

    id: str = Field(primary_key=True)  # UUID
    user_id: str = Field(index=True)
    title: str | None = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

### Messages Table

```python
class Message(SQLModel, table=True):
    __tablename__ = "messages"

    id: int | None = Field(default=None, primary_key=True)
    conversation_id: str = Field(foreign_key="conversations.id", index=True)
    role: str = Field()  # user, assistant, tool
    content: str = Field()
    tool_calls: str | None = Field(default=None)  # JSON serialized
    created_at: datetime = Field(default_factory=datetime.utcnow)
```

## MCP Server Specification

### Server Configuration

```python
# MCP Server runs as a subprocess or stdio-based server
# Transport: stdio (for local) or SSE (for remote)
server_name = "todo-mcp-server"
server_version = "1.0.0"
```

### MCP Tools

#### 1. add_task

**Purpose**: Create a new task in the database.

```python
@mcp_server.tool()
async def add_task(
    title: str,
    description: str | None = None,
    priority: str = "medium",
    due_date: str | None = None,
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
```

#### 2. list_tasks

**Purpose**: Retrieve tasks with optional filtering.

```python
@mcp_server.tool()
async def list_tasks(
    user_id: str = "default",
    completed: bool | None = None,
    priority: str | None = None,
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
```

#### 3. complete_task

**Purpose**: Mark a task as completed.

```python
@mcp_server.tool()
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
```

#### 4. delete_task

**Purpose**: Remove a task from the database.

```python
@mcp_server.tool()
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
```

#### 5. update_task

**Purpose**: Modify an existing task.

```python
@mcp_server.tool()
async def update_task(
    task_id: int,
    title: str | None = None,
    description: str | None = None,
    priority: str | None = None,
    due_date: str | None = None,
    completed: bool | None = None,
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
```

## FastAPI Backend Specification

### API Endpoints

#### Chat Endpoint

```python
@app.post("/api/chat")
async def chat(request: ChatRequest) -> StreamingResponse:
    """
    Main chat endpoint that processes user messages through OpenAI Agents.

    Request Body:
        - message: str - User's message
        - conversation_id: str | None - Existing conversation ID
        - user_id: str - User identifier

    Response:
        - Server-Sent Events stream with assistant responses
    """
```

#### Conversation Management

```python
@app.get("/api/conversations")
async def list_conversations(user_id: str) -> list[Conversation]:
    """List all conversations for a user."""

@app.get("/api/conversations/{conversation_id}")
async def get_conversation(conversation_id: str) -> ConversationWithMessages:
    """Get a conversation with all its messages."""

@app.delete("/api/conversations/{conversation_id}")
async def delete_conversation(conversation_id: str) -> dict:
    """Delete a conversation and all its messages."""
```

#### Health Check

```python
@app.get("/health")
async def health_check() -> dict:
    """Health check endpoint for monitoring."""
```

### OpenAI Agents SDK Integration

```python
from openai import OpenAI
from agents import Agent, Runner

# Agent configuration
todo_agent = Agent(
    name="Todo Assistant",
    instructions="""You are a helpful task management assistant.
    You help users manage their todo lists by adding, listing,
    completing, updating, and deleting tasks.
    Be concise and helpful in your responses.""",
    model="gpt-4o-mini",
    tools=[mcp_client.get_tools()]  # MCP tools loaded dynamically
)

# Runner for executing agent with tools
runner = Runner(agent=todo_agent)
```

### Stateless Architecture

The backend is completely stateless:

1. **No in-memory state**: All conversation history loaded from DB per request
2. **No session storage**: User identification via API headers/tokens
3. **Horizontal scaling**: Any instance can handle any request
4. **Database-driven**: All state persisted to Neon PostgreSQL

```python
async def process_chat(message: str, conversation_id: str, user_id: str):
    # Load conversation history from database
    history = await load_conversation_history(conversation_id)

    # Process with OpenAI Agent
    response = await runner.run(
        messages=history + [{"role": "user", "content": message}]
    )

    # Persist new messages to database
    await save_messages(conversation_id, response.messages)

    return response
```

## Frontend Specification (OpenAI ChatKit UI)

### Components

1. **ChatContainer**: Main chat interface wrapper
2. **MessageList**: Displays conversation history
3. **MessageInput**: Text input with send button
4. **TaskList**: Optional sidebar showing current tasks
5. **ConversationSidebar**: List of past conversations

### Integration

```typescript
// ChatKit configuration
import { Chat, Message, useChat } from '@openai/chatkit';

const TodoChat = () => {
  const { messages, sendMessage, isLoading } = useChat({
    endpoint: '/api/chat',
    conversationId: currentConversation,
  });

  return (
    <Chat
      messages={messages}
      onSendMessage={sendMessage}
      isLoading={isLoading}
      placeholder="Ask me to manage your tasks..."
    />
  );
};
```

## Environment Variables

```bash
# Database
DATABASE_URL=postgresql://user:pass@host/dbname?sslmode=require

# OpenAI
OPENAI_API_KEY=sk-...

# Server
HOST=0.0.0.0
PORT=8000
DEBUG=false

# MCP Server
MCP_SERVER_PATH=./mcp_server.py
```

## Non-Functional Requirements

### Performance
- Chat response latency < 2 seconds for non-tool calls
- Database queries optimized with proper indexing
- Connection pooling for PostgreSQL

### Security
- API key validation for all endpoints
- SQL injection prevention via SQLModel ORM
- Input validation and sanitization

### Scalability
- Stateless design enables horizontal scaling
- Neon PostgreSQL auto-scales storage
- No sticky sessions required

### Reliability
- Health check endpoint for load balancers
- Graceful error handling with user-friendly messages
- Database connection retry logic

## File Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── config.py            # Environment configuration
│   ├── database.py          # SQLModel database setup
│   ├── models/
│   │   ├── __init__.py
│   │   ├── task.py          # Task model
│   │   ├── conversation.py  # Conversation model
│   │   └── message.py       # Message model
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── chat.py          # Chat endpoints
│   │   └── conversations.py # Conversation endpoints
│   ├── services/
│   │   ├── __init__.py
│   │   ├── agent.py         # OpenAI Agent service
│   │   └── mcp_client.py    # MCP client integration
│   └── mcp_server/
│       ├── __init__.py
│       ├── server.py        # MCP server implementation
│       └── tools.py         # MCP tool definitions
├── requirements.txt
└── Dockerfile

frontend/
├── src/
│   ├── app/
│   │   ├── page.tsx         # Main chat page
│   │   └── layout.tsx       # App layout
│   ├── components/
│   │   ├── Chat.tsx         # Chat component
│   │   ├── MessageList.tsx  # Message display
│   │   └── TaskSidebar.tsx  # Task list sidebar
│   └── lib/
│       └── api.ts           # API client
├── package.json
└── next.config.js
```

## Success Criteria

1. User can chat with AI to manage tasks naturally
2. All CRUD operations work via MCP tools
3. Conversations persist across sessions
4. System scales horizontally with no session affinity
5. Response times meet performance requirements
6. Clean, intuitive ChatKit-based UI
