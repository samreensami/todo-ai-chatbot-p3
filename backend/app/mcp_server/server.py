"""MCP Server implementation for Todo AI Chatbot."""
import json
from typing import Any
from mcp.server import Server
from mcp.types import Tool, TextContent
from mcp.server.stdio import stdio_server

from app.mcp_server.tools import (
    add_task,
    list_tasks,
    complete_task,
    delete_task,
    update_task,
)

# Create MCP server instance
mcp_server = Server("todo-mcp-server")


# Define tool schemas
TOOLS = [
    Tool(
        name="add_task",
        description="Add a new task to the todo list.",
        inputSchema={
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "The task title (required)"
                },
                "description": {
                    "type": "string",
                    "description": "Optional task description"
                },
                "priority": {
                    "type": "string",
                    "enum": ["low", "medium", "high"],
                    "description": "Task priority - low, medium, or high",
                    "default": "medium"
                },
                "due_date": {
                    "type": "string",
                    "description": "Optional due date in ISO format (YYYY-MM-DD)"
                },
                "user_id": {
                    "type": "string",
                    "description": "User identifier for multi-user support",
                    "default": "default"
                }
            },
            "required": ["title"]
        }
    ),
    Tool(
        name="list_tasks",
        description="List tasks with optional filters.",
        inputSchema={
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "string",
                    "description": "User identifier",
                    "default": "default"
                },
                "completed": {
                    "type": "boolean",
                    "description": "Filter by completion status (true/false, omit for all)"
                },
                "priority": {
                    "type": "string",
                    "enum": ["low", "medium", "high"],
                    "description": "Filter by priority level"
                },
                "limit": {
                    "type": "integer",
                    "description": "Maximum number of tasks to return",
                    "default": 50
                }
            }
        }
    ),
    Tool(
        name="complete_task",
        description="Mark a task as completed.",
        inputSchema={
            "type": "object",
            "properties": {
                "task_id": {
                    "type": "integer",
                    "description": "The ID of the task to complete"
                },
                "user_id": {
                    "type": "string",
                    "description": "User identifier for authorization",
                    "default": "default"
                }
            },
            "required": ["task_id"]
        }
    ),
    Tool(
        name="delete_task",
        description="Delete a task from the todo list.",
        inputSchema={
            "type": "object",
            "properties": {
                "task_id": {
                    "type": "integer",
                    "description": "The ID of the task to delete"
                },
                "user_id": {
                    "type": "string",
                    "description": "User identifier for authorization",
                    "default": "default"
                }
            },
            "required": ["task_id"]
        }
    ),
    Tool(
        name="update_task",
        description="Update an existing task.",
        inputSchema={
            "type": "object",
            "properties": {
                "task_id": {
                    "type": "integer",
                    "description": "The ID of the task to update"
                },
                "title": {
                    "type": "string",
                    "description": "New title (optional)"
                },
                "description": {
                    "type": "string",
                    "description": "New description (optional)"
                },
                "priority": {
                    "type": "string",
                    "enum": ["low", "medium", "high"],
                    "description": "New priority level (optional)"
                },
                "due_date": {
                    "type": "string",
                    "description": "New due date in ISO format (optional)"
                },
                "completed": {
                    "type": "boolean",
                    "description": "New completion status (optional)"
                },
                "user_id": {
                    "type": "string",
                    "description": "User identifier for authorization",
                    "default": "default"
                }
            },
            "required": ["task_id"]
        }
    ),
]

# Tool name to function mapping
TOOL_HANDLERS = {
    "add_task": add_task,
    "list_tasks": list_tasks,
    "complete_task": complete_task,
    "delete_task": delete_task,
    "update_task": update_task,
}


@mcp_server.list_tools()
async def list_tools() -> list[Tool]:
    """Return list of available tools."""
    return TOOLS


@mcp_server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    """Execute a tool and return the result."""
    if name not in TOOL_HANDLERS:
        return [TextContent(type="text", text=json.dumps({"error": f"Unknown tool: {name}"}))]

    handler = TOOL_HANDLERS[name]
    result = await handler(**arguments)
    return [TextContent(type="text", text=json.dumps(result, default=str))]


def get_tools_for_openai() -> list[dict]:
    """Convert MCP tools to OpenAI function calling format."""
    return [
        {
            "type": "function",
            "function": {
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.inputSchema,
            }
        }
        for tool in TOOLS
    ]


async def run_server():
    """Run the MCP server via stdio."""
    async with stdio_server() as (read_stream, write_stream):
        await mcp_server.run(read_stream, write_stream, mcp_server.create_initialization_options())


if __name__ == "__main__":
    import asyncio
    asyncio.run(run_server())
