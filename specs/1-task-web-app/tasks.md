# Tasks: Task Web App Implementation

**Input**: Design documents from `/specs/1-task-web-app/`
**Prerequisites**: plan.md, spec.md, data-model.md

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Parallel task
- **[Story]**: US1 (Task Management), US2 (Auth), US3 (Categorization)

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and monorepo structure

- [ ] T001 Create `backend/` and `frontend/` directory structure per plan
- [ ] T002 Initialize FastAPI project in `backend/` with `pyproject.toml`
- [ ] T003 Initialize Next.js 16+ project in `frontend/` with TypeScript
- [ ] T004 [P] Configure root-level `.env.template` and workspace configuration

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure for Auth, DB, and Type Sync

- [ ] T005 [P] Setup Neon PostgreSQL connection in `backend/core/database.py`
- [ ] T006 Initialize Alembic in `backend/alembic/` for migrations
- [ ] T007 Implement JWT verification middleware in `backend/core/security.py`
- [ ] T008 [P] Setup Better Auth client in `frontend/lib/auth-client.ts`
- [ ] T009 Create `.claude/skills/api-generator` script for type synchronization

**Checkpoint**: Foundation ready - user story implementation can now begin.

---

## Phase 3: User Story 2 - User Authentication (Priority: P1) 🎯 MVP

**Goal**: Register, Login, and Secure endpoints

- [ ] T010 [P] [US2] Create User model in `backend/models/user.py`
- [ ] T011 [US2] Create User registration and login endpoints in `backend/routes/auth.py`
- [ ] T012 [US2] Setup Better Auth route handlers in `frontend/app/api/auth/[...all]/route.ts`
- [ ] T013 [US2] Implement Login and Signup pages in `frontend/app/auth/`
- [ ] T014 [US2] Verify JWT access from frontend to protected backend routes

**Checkpoint**: Users can securely authenticate.

---

## Phase 4: User Story 1 - Task Management (Priority: P1) 🎯 MVP

**Goal**: Core CRUD operations for tasks

- [ ] T015 [P] [US1] Create Task model in `backend/models/task.py`
- [ ] T016 [US1] Generate and run Alembic migration for tasks table
- [ ] T017 [US1] Implement CRUD endpoints in `backend/routes/tasks.py` (protected by JWT)
- [ ] T018 [US1] Run `api-generator` skill to sync task types to `frontend/lib/generated/`
- [ ] T019 [US1] Build Task Dashboard in `frontend/app/dashboard/page.tsx`
- [ ] T020 [US1] Implement Add/Edit task forms and Delete functionality in frontend

**Checkpoint**: Users can manage their own tasks.

---

## Phase 5: User Story 3 - Task Categorization (Priority: P3)

**Goal**: Organize tasks by categories

- [ ] T021 [US3] Update Task model and API to support `category` field
- [ ] T022 [US3] Add category selection to frontend task forms
- [ ] T023 [US3] Implement category filtering on the dashboard

---

## Phase 6: Polish & Deployment

- [ ] T024 Add loading states and error toast notifications in frontend
- [ ] T025 Performance check: Verify task list loads < 500ms
- [ ] T026 Update `quickstart.md` with final installation steps
- [ ] T027 Final security review of JWT verification logic
