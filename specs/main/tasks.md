# Tasks: Phase III Todo AI Chatbot

**Input**: Design documents from `/specs/main/`
**Prerequisites**: plan.md, ai_chatbot_spec.md, research.md, data-model.md, contracts/

**Tests**: Not explicitly requested - test tasks omitted.

**Organization**: Tasks organized by user story for independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions

- **Backend**: `backend/app/`
- **Frontend**: `frontend/src/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization, dependencies, and basic structure

- [ ] T001 Create backend directory structure per plan in backend/app/
- [ ] T002 [P] Create requirements.txt with FastAPI, SQLModel, OpenAI, MCP dependencies in backend/requirements.txt
- [ ] T003 [P] Create frontend Next.js project structure in frontend/
- [ ] T004 [P] Create .env.example with DATABASE_URL, OPENAI_API_KEY placeholders in backend/.env.example
- [ ] T005 [P] Create config.py with pydantic-settings for environment management in backend/app/config.py

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Database connection and models that ALL user stories depend on

**CRITICAL**: No user story work can begin until this phase is complete

- [ ] T006 Create async database connection with SQLModel engine in backend/app/database.py
- [ ] T007 [P] Create Task SQLModel in backend/app/models/task.py
- [ ] T008 [P] Create Conversation SQLModel in backend/app/models/conversation.py
- [ ] T009 [P] Create Message SQLModel in backend/app/models/message.py
- [ ] T010 Create models __init__.py exporting all models in backend/app/models/__init__.py
- [ ] T011 Create FastAPI app skeleton with CORS and health endpoint in backend/app/main.py
- [ ] T012 [P] Create routers __init__.py in backend/app/routers/__init__.py
- [ ] T013 [P] Create services __init__.py in backend/app/services/__init__.py

**Checkpoint**: Foundation ready - database connected, models defined, FastAPI app running

---

## Phase 3: User Story 1 - MCP Server with Task Tools (Priority: P1)

**Goal**: Implement MCP server with all 5 task management tools (add_task, list_tasks, complete_task, delete_task, update_task)

**Independent Test**: Run MCP server standalone, call tools directly via MCP protocol

### Implementation for User Story 1

- [ ] T014 [P] [US1] Create MCP server __init__.py in backend/app/mcp_server/__init__.py
- [ ] T015 [US1] Create MCP server main with tool registration in backend/app/mcp_server/server.py
- [ ] T016 [US1] Implement add_task MCP tool in backend/app/mcp_server/tools.py
- [ ] T017 [US1] Implement list_tasks MCP tool in backend/app/mcp_server/tools.py
- [ ] T018 [US1] Implement complete_task MCP tool in backend/app/mcp_server/tools.py
- [ ] T019 [US1] Implement delete_task MCP tool in backend/app/mcp_server/tools.py
- [ ] T020 [US1] Implement update_task MCP tool in backend/app/mcp_server/tools.py

**Checkpoint**: MCP server runs with all 5 tools, can be tested independently

---

## Phase 4: User Story 2 - AI Chat Endpoint (Priority: P2)

**Goal**: Implement FastAPI chat endpoint with OpenAI Agents SDK integration

**Independent Test**: POST to /api/chat with message, receive SSE stream response with tool calls

### Implementation for User Story 2

- [ ] T021 [US2] Create MCP client service for loading tools in backend/app/services/mcp_client.py
- [ ] T022 [US2] Create OpenAI Agent service with tool integration in backend/app/services/agent.py
- [ ] T023 [US2] Create chat router with POST /api/chat SSE endpoint in backend/app/routers/chat.py
- [ ] T024 [US2] Integrate chat router into main.py in backend/app/main.py
- [ ] T025 [US2] Implement stateless conversation loading from database in backend/app/services/agent.py
- [ ] T026 [US2] Implement message persistence after agent response in backend/app/services/agent.py

**Checkpoint**: Chat endpoint works, AI responds and can call MCP tools

---

## Phase 5: User Story 3 - Conversation Management (Priority: P3)

**Goal**: Implement conversation CRUD endpoints for persistence

**Independent Test**: Create conversation, add messages, list conversations, delete conversation

### Implementation for User Story 3

- [ ] T027 [US3] Create conversations router with list endpoint in backend/app/routers/conversations.py
- [ ] T028 [US3] Implement get conversation with messages endpoint in backend/app/routers/conversations.py
- [ ] T029 [US3] Implement delete conversation endpoint in backend/app/routers/conversations.py
- [ ] T030 [US3] Integrate conversations router into main.py in backend/app/main.py

**Checkpoint**: Full conversation persistence working, stateless architecture verified

---

## Phase 6: User Story 4 - Frontend Chat UI (Priority: P4)

**Goal**: Implement Next.js frontend with chat interface

**Independent Test**: Open browser, send chat message, see AI response with task operations

### Implementation for User Story 4

- [ ] T031 [P] [US4] Create Next.js layout with Tailwind in frontend/src/app/layout.tsx
- [ ] T032 [P] [US4] Create API client with fetch for chat endpoint in frontend/src/lib/api.ts
- [ ] T033 [US4] Create MessageList component for displaying messages in frontend/src/components/MessageList.tsx
- [ ] T034 [US4] Create Chat component with input and SSE handling in frontend/src/components/Chat.tsx
- [ ] T035 [US4] Create main page integrating Chat component in frontend/src/app/page.tsx
- [ ] T036 [US4] Create next.config.js with API proxy configuration in frontend/next.config.js
- [ ] T037 [P] [US4] Create package.json with Next.js and dependencies in frontend/package.json

**Checkpoint**: Full end-to-end chat working in browser

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Error handling, validation, and production readiness

- [ ] T038 [P] Add input validation to all MCP tools in backend/app/mcp_server/tools.py
- [ ] T039 [P] Add error handling middleware to FastAPI in backend/app/main.py
- [ ] T040 [P] Add loading states and error display to frontend in frontend/src/components/Chat.tsx
- [ ] T041 Run quickstart.md validation to verify full setup works

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Story 1 (Phase 3)**: Depends on Foundational - MCP Server
- **User Story 2 (Phase 4)**: Depends on US1 (needs MCP tools)
- **User Story 3 (Phase 5)**: Depends on Foundational only
- **User Story 4 (Phase 6)**: Depends on US2 (needs chat endpoint)
- **Polish (Phase 7)**: Depends on all user stories

### User Story Dependencies

```
Foundational (Phase 2)
       │
       ├── US1: MCP Server (Phase 3)
       │         │
       │         └── US2: Chat Endpoint (Phase 4)
       │                   │
       │                   └── US4: Frontend (Phase 6)
       │
       └── US3: Conversations (Phase 5) [Independent]
```

### Parallel Opportunities

**Phase 1 (Setup)**:
```
T002, T003, T004, T005 can run in parallel
```

**Phase 2 (Foundational)**:
```
T007, T008, T009 (models) can run in parallel
T012, T013 (init files) can run in parallel
```

**Phase 6 (Frontend)**:
```
T031, T032, T037 can run in parallel
```

---

## Parallel Example: Phase 2 (Foundational)

```bash
# Launch all models in parallel:
Task: "Create Task SQLModel in backend/app/models/task.py"
Task: "Create Conversation SQLModel in backend/app/models/conversation.py"
Task: "Create Message SQLModel in backend/app/models/message.py"
```

---

## Implementation Strategy

### MVP First (US1 + US2)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: MCP Server (US1)
4. Complete Phase 4: Chat Endpoint (US2)
5. **STOP and VALIDATE**: Test chat with MCP tools via curl/API
6. Can demo backend-only MVP

### Full Implementation

1. Setup + Foundational → Foundation ready
2. US1 (MCP Server) → Test tools independently
3. US2 (Chat Endpoint) → Test chat via API
4. US3 (Conversations) → Test persistence (can parallel with US2)
5. US4 (Frontend) → Full UI working
6. Polish → Production ready

---

## Summary

| Phase | Tasks | Parallel Tasks |
|-------|-------|----------------|
| Setup | 5 | 4 |
| Foundational | 8 | 5 |
| US1: MCP Server | 7 | 1 |
| US2: Chat Endpoint | 6 | 0 |
| US3: Conversations | 4 | 0 |
| US4: Frontend | 7 | 3 |
| Polish | 4 | 3 |
| **Total** | **41** | **16** |

**MVP Scope**: Phases 1-4 (26 tasks) delivers working AI chat with MCP tools
