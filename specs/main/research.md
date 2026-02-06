# Research: Phase III Todo AI Chatbot

**Date**: 2026-02-05 | **Feature**: AI-powered Task Management Chatbot

## Research Areas

### 1. MCP (Model Context Protocol) Implementation

**Question**: How to implement MCP server with Python for tool execution?

**Findings**:
- MCP Python SDK (`mcp`) provides `@server.tool()` decorator for defining tools
- Server can run via stdio (local) or SSE (remote) transport
- Tools are async functions that return structured responses
- MCP handles serialization/deserialization automatically

**Decision**: Use `mcp` package with stdio transport

**Code Pattern**:
```python
from mcp.server import Server
from mcp.server.stdio import stdio_server

server = Server("todo-mcp-server")

@server.tool()
async def add_task(title: str, description: str = None) -> dict:
    # Implementation
    return {"id": task.id, "title": task.title}
```

### 2. OpenAI Agents SDK with MCP Integration

**Question**: How to connect OpenAI Agents SDK with MCP tools?

**Findings**:
- OpenAI Agents SDK supports external tool providers
- MCP tools can be converted to OpenAI function calling format
- Use `Runner` class for executing agent with tools
- Streaming supported via `Runner.run_stream()`

**Decision**: Create MCP client that loads tools and converts to Agent-compatible format

**Integration Pattern**:
```python
from agents import Agent, Runner
from agents.mcp import MCPServerStdio

async with MCPServerStdio(command="python", args=["mcp_server.py"]) as mcp:
    agent = Agent(
        name="Todo Assistant",
        tools=mcp.list_tools()
    )
    runner = Runner(agent=agent)
```

### 3. SQLModel Async Pattern with Neon

**Question**: Best practices for async SQLModel with Neon PostgreSQL?

**Findings**:
- Use `create_async_engine` with `asyncpg` driver
- Neon requires SSL connection (`sslmode=require`)
- Connection pooling handled by SQLAlchemy async engine
- Use `AsyncSession` for all database operations

**Decision**: Async SQLModel with connection pooling

**Connection Pattern**:
```python
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

DATABASE_URL = "postgresql+asyncpg://user:pass@host/db?ssl=require"

engine = create_async_engine(DATABASE_URL, pool_size=5, max_overflow=10)
async_session = async_sessionmaker(engine, class_=AsyncSession)
```

### 4. Stateless Chat Architecture

**Question**: How to maintain conversation context without server state?

**Findings**:
- Store all messages in database with conversation_id
- Load full conversation history on each request
- OpenAI API accepts message array for context
- Truncate old messages if context window exceeded

**Decision**: Database-first conversation management

**Pattern**:
```python
async def chat(message: str, conversation_id: str):
    # Load history from DB
    messages = await db.get_messages(conversation_id)

    # Add new user message
    messages.append({"role": "user", "content": message})

    # Process with agent
    response = await runner.run(messages=messages)

    # Save all new messages to DB
    await db.save_messages(conversation_id, response.new_messages)
```

### 5. SSE Streaming for Chat Responses

**Question**: How to stream chat responses to frontend?

**Findings**:
- FastAPI supports `StreamingResponse` with SSE
- Use `text/event-stream` content type
- Format: `data: {json}\n\n`
- Frontend uses `EventSource` or fetch with reader

**Decision**: SSE streaming with JSON payloads

**Pattern**:
```python
from fastapi.responses import StreamingResponse

async def stream_chat():
    async def generate():
        async for chunk in runner.run_stream(messages):
            yield f"data: {json.dumps(chunk)}\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")
```

## Dependencies Resolved

| Package | Version | Purpose |
|---------|---------|---------|
| fastapi | ^0.109.0 | Web framework |
| uvicorn | ^0.27.0 | ASGI server |
| sqlmodel | ^0.0.14 | ORM with Pydantic |
| asyncpg | ^0.29.0 | Async PostgreSQL driver |
| openai-agents | ^0.1.0 | Agent orchestration |
| mcp | ^1.0.0 | MCP server/client |
| python-dotenv | ^1.0.0 | Environment config |
| pydantic-settings | ^2.1.0 | Settings management |

## Open Questions

None - all technical decisions resolved.
