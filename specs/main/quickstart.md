# Quickstart: Phase III Todo AI Chatbot

## Prerequisites

- Python 3.12+
- Node.js 18+
- Neon PostgreSQL database
- OpenAI API key

## Environment Setup

1. Create `.env` file in project root:

```bash
# Database
DATABASE_URL=postgresql+asyncpg://user:password@host/dbname?ssl=require

# OpenAI
OPENAI_API_KEY=sk-your-api-key

# Server
HOST=0.0.0.0
PORT=8000
DEBUG=true
```

## Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or: venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Run database migrations (tables auto-created by SQLModel)
python -c "from app.database import init_db; import asyncio; asyncio.run(init_db())"

# Start the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Frontend Setup

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

## Verify Installation

1. **Health Check**:
```bash
curl http://localhost:8000/health
# Expected: {"status":"healthy","timestamp":"..."}
```

2. **Test Chat** (using curl):
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Add a task to buy groceries", "user_id": "test-user"}'
```

3. **Open Frontend**:
Navigate to http://localhost:3000

## Project Structure

```
.
├── backend/
│   ├── app/
│   │   ├── main.py           # FastAPI app
│   │   ├── config.py         # Settings
│   │   ├── database.py       # DB connection
│   │   ├── models/           # SQLModel entities
│   │   ├── routers/          # API endpoints
│   │   ├── services/         # Business logic
│   │   └── mcp_server/       # MCP tools
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── app/              # Next.js pages
│   │   ├── components/       # React components
│   │   └── lib/              # Utilities
│   └── package.json
└── specs/                    # Documentation
```

## Common Commands

| Command | Description |
|---------|-------------|
| `uvicorn app.main:app --reload` | Start backend dev server |
| `npm run dev` | Start frontend dev server |
| `pytest` | Run backend tests |
| `npm test` | Run frontend tests |

## Troubleshooting

### Database Connection Issues
- Verify `DATABASE_URL` is correct
- Ensure Neon database is active
- Check SSL mode is enabled

### OpenAI API Errors
- Verify `OPENAI_API_KEY` is valid
- Check API quota/limits

### MCP Server Issues
- Ensure MCP server starts with backend
- Check tool definitions in `mcp_server/tools.py`
