"""FastAPI application for Todo AI Chatbot."""
from contextlib import asynccontextmanager
from datetime import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.database import init_db
from app.routers import chat_router, conversations_router, dashboard_router, auth_router

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler - initialize DB on startup."""
    # Startup
    print("Initializing database...")
    await init_db()
    print("Database initialized successfully!")
    yield
    # Shutdown
    print("Shutting down...")


# Create FastAPI app
app = FastAPI(
    title="Todo AI Chatbot API",
    description="AI-powered task management chatbot with MCP tools",
    version="1.0.0",
    lifespan=lifespan,
)

# Configure CORS - fully permissive for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)  # /auth/login, /auth/register, /auth/logout
app.include_router(chat_router)  # /api/chat
app.include_router(conversations_router)  # /api/conversations
app.include_router(dashboard_router)  # /dashboard/stats, /dashboard/tasks


@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring."""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "todo-ai-chatbot",
    }


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": "Todo AI Chatbot API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
    )
