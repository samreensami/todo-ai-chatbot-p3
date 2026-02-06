# Phase III: Todo AI Chatbot - Quick Start

## Architecture
- **Backend**: FastAPI + Gemini AI + MCP Tools
- **Frontend**: Next.js Chat UI
- **Database**: Neon PostgreSQL (stateless)

## URLs
- **Backend API**: http://localhost:8000
- **Frontend UI**: http://localhost:3007
- **API Docs**: http://localhost:8000/docs
- **Chat Page**: http://localhost:3007/chat

## Start the Servers

### Option 1: Windows Batch Files
```
# Terminal 1 - Backend
start-backend.bat

# Terminal 2 - Frontend
start-frontend.bat
```

### Option 2: Manual Commands

**Terminal 1 - Backend:**
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## Test the API

```bash
# Health check
curl http://localhost:8000/health

# Chat with AI
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Add a task to buy groceries", "user_id": "demo"}'
```

## MCP Tools Available
1. **add_task** - Create new tasks
2. **list_tasks** - List tasks with filters
3. **complete_task** - Mark task as done
4. **delete_task** - Remove task
5. **update_task** - Modify task details

## Example Chat Commands
- "Show me all my tasks"
- "Add a task: Buy groceries with high priority"
- "Mark task #1 as complete"
- "Delete task #2"
- "Show my pending tasks"
- "Update task #1 priority to high"

## Tech Stack
- FastAPI (Backend)
- Gemini 1.5 Flash (AI)
- SQLModel + asyncpg (Database)
- Neon PostgreSQL (Cloud DB)
- Next.js 16 (Frontend)
- Tailwind CSS (Styling)
