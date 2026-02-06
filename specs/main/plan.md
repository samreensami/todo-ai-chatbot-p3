# Implementation Plan: Phase III Todo AI Chatbot

**Branch**: `main` | **Date**: 2026-02-05 | **Spec**: [specs/ai_chatbot_spec.md](../ai_chatbot_spec.md)
**Input**: Feature specification from `/specs/ai_chatbot_spec.md`

## Summary

Build a stateless AI-powered chatbot for task management using FastAPI backend, OpenAI Agents SDK for AI orchestration, and MCP (Model Context Protocol) Server for tool execution. The system persists all conversation and task data to Neon PostgreSQL and provides a modern chat interface via OpenAI ChatKit UI.

## Technical Context

**Language/Version**: Python 3.12, TypeScript 5.x
**Primary Dependencies**: FastAPI, OpenAI Agents SDK, MCP Python SDK, SQLModel, Next.js
**Storage**: Neon PostgreSQL (Serverless)
**Testing**: pytest (backend), Jest (frontend)
**Target Platform**: Linux server (backend), Web browser (frontend)
**Project Type**: Web application (monorepo with backend + frontend)
**Performance Goals**: < 2s chat response latency, optimized DB queries with indexing
**Constraints**: Stateless architecture, no in-memory state, horizontal scaling ready
**Scale/Scope**: Multi-user support, conversation persistence, 5 MCP tools

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Next.js Frontend Excellence | ✅ PASS | Using Next.js App Router with TypeScript |
| II. FastAPI Backend Architecture | ✅ PASS | FastAPI with OpenAPI docs, Pydantic validation |
| III. Neon DB & Database Integrity | ✅ PASS | SQLModel ORM with Neon PostgreSQL |
| IV. Type Safety (End-to-End) | ✅ PASS | TypeScript frontend, Python type hints backend |
| V. Test-Driven Development | ✅ PASS | pytest + Jest testing strategy |

## Project Structure

### Documentation (this feature)

```text
specs/main/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output (OpenAPI specs)
└── tasks.md             # Phase 2 output
```

### Source Code (repository root)

```text
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry
│   ├── config.py            # Environment configuration
│   ├── database.py          # SQLModel database setup
│   ├── models/
│   │   ├── __init__.py
│   │   ├── task.py          # Task SQLModel
│   │   ├── conversation.py  # Conversation SQLModel
│   │   └── message.py       # Message SQLModel
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── chat.py          # Chat endpoints
│   │   └── conversations.py # Conversation CRUD
│   ├── services/
│   │   ├── __init__.py
│   │   ├── agent.py         # OpenAI Agent service
│   │   └── mcp_client.py    # MCP client integration
│   └── mcp_server/
│       ├── __init__.py
│       ├── server.py        # MCP server implementation
│       └── tools.py         # MCP tool definitions
├── requirements.txt
└── tests/

frontend/
├── src/
│   ├── app/
│   │   ├── page.tsx         # Main chat page
│   │   └── layout.tsx       # App layout
│   ├── components/
│   │   ├── Chat.tsx         # Chat component
│   │   └── MessageList.tsx  # Message display
│   └── lib/
│       └── api.ts           # API client
├── package.json
└── next.config.js
```

**Structure Decision**: Web application structure with separate backend/ and frontend/ directories following monorepo pattern per constitution requirements.

## Complexity Tracking

> No violations - all principles satisfied.

---

# Phase 0: Research

## Technology Decisions

### 1. MCP Server Implementation

**Decision**: Use `mcp` Python SDK with stdio transport for local development
**Rationale**:
- Official MCP Python SDK provides clean decorator-based tool definitions
- stdio transport works seamlessly with OpenAI Agents SDK
- SSE transport available for production deployments
**Alternatives Considered**:
- Custom tool implementation: Rejected - MCP provides standardized protocol
- REST-based tools: Rejected - MCP offers better AI integration

### 2. OpenAI Agents SDK Integration

**Decision**: Use OpenAI Agents SDK with function calling for MCP tool execution
**Rationale**:
- Native support for tool/function calling
- Streaming response support for real-time chat
- Built-in conversation management
**Alternatives Considered**:
- LangChain: Rejected - adds unnecessary abstraction layer
- Direct OpenAI API: Rejected - Agents SDK provides better tool orchestration

### 3. Database Connection Strategy

**Decision**: SQLModel with async engine and connection pooling
**Rationale**:
- SQLModel combines SQLAlchemy + Pydantic for type-safe ORM
- Async support for non-blocking database operations
- Connection pooling for efficient resource usage
**Alternatives Considered**:
- Raw asyncpg: Rejected - loses ORM benefits
- Prisma: Rejected - better Python ecosystem integration with SQLModel

### 4. Stateless Architecture Pattern

**Decision**: Load conversation history from DB per request, no server-side sessions
**Rationale**:
- Enables horizontal scaling without session affinity
- Neon PostgreSQL handles connection pooling at database level
- Simplifies deployment and failover
**Alternatives Considered**:
- Redis session store: Rejected - adds infrastructure complexity
- In-memory caching: Rejected - breaks stateless requirement

---

# Phase 1: Design & Contracts

## Data Model

See [data-model.md](./data-model.md) for complete entity definitions.

### Core Entities

1. **Task**: User's todo items with title, description, priority, due_date, completion status
2. **Conversation**: Chat session container with user association
3. **Message**: Individual messages in a conversation (user, assistant, tool roles)

### Relationships

```
User (implicit via user_id)
  └── has many → Conversations
        └── has many → Messages
  └── has many → Tasks
```

## API Contracts

See [contracts/](./contracts/) directory for OpenAPI specifications.

### Endpoints Summary

| Method | Path | Description |
|--------|------|-------------|
| POST | /api/chat | Send message, receive SSE stream response |
| GET | /api/conversations | List user's conversations |
| GET | /api/conversations/{id} | Get conversation with messages |
| DELETE | /api/conversations/{id} | Delete conversation |
| GET | /health | Health check |

### MCP Tools

| Tool | Parameters | Description |
|------|------------|-------------|
| add_task | title, description?, priority?, due_date?, user_id | Create new task |
| list_tasks | user_id, completed?, priority?, limit? | List tasks with filters |
| complete_task | task_id, user_id | Mark task as completed |
| delete_task | task_id, user_id | Remove task |
| update_task | task_id, title?, description?, priority?, due_date?, completed?, user_id | Update task fields |

## Quickstart

See [quickstart.md](./quickstart.md) for setup and running instructions.
