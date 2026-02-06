import json
import cohere
from typing import AsyncGenerator, Optional
from datetime import datetime
from sqlmodel import select

from app.config import get_settings
from app.database import get_db_session
from app.models import Conversation, Message, Task
from app.mcp_server.tools import (
    add_task,
    list_tasks,
    complete_task,
    delete_task,
    update_task,
)

settings = get_settings()

# Tool Mapping
TOOL_FUNCTIONS = {
    "add_task": add_task,
    "list_tasks": list_tasks,
    "complete_task": complete_task,
    "delete_task": delete_task,
    "update_task": update_task,
}

# 1. SMART SYSTEM PROMPT (User ko tang nahi karega)
SYSTEM_PROMPT = """You are a helpful task management assistant.
- When adding tasks: ALWAYS use priority='medium' if the user doesn't specify one. Never ask for priority.
- When deleting or completing: ALWAYS call list_tasks first to find the ID of the task, then use that ID.
- Be very brief. Confirm actions with 'Done!' or 'Task added/deleted'."""

# 2. COHERE TOOLS DEFINITION (AI ko batata hai kya kya kar sakta hai)
COHERE_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "add_task",
            "description": "Add a new task",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "description": {"type": "string"},
                    "priority": {"type": "string", "enum": ["low", "medium", "high"]},
                    "due_date": {"type": "string"}
                },
                "required": ["title"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_tasks",
            "description": "List all tasks"
        }
    },
    {
        "type": "function",
        "function": {
            "name": "complete_task",
            "description": "Mark a task as done",
            "parameters": {
                "type": "object",
                "properties": {"task_id": {"type": "integer"}},
                "required": ["task_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "delete_task",
            "description": "Delete a task",
            "parameters": {
                "type": "object",
                "properties": {"task_id": {"type": "integer"}},
                "required": ["task_id"]
            }
        }
    }
]

class TodoAgent:
    def __init__(self):
        self.client = cohere.ClientV2(api_key=settings.cohere_api_key)
        self.model = "command-r7b-12-2024"

    async def chat(self, message: str, conversation_id: Optional[str], user_id: str) -> AsyncGenerator[str, None]:
        try:
            # First AI Response
            res = self.client.chat(
                model=self.model,
                messages=[{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": message}],
                tools=COHERE_TOOLS
            )

            # Handle Tool Calls (Add/Delete/List)
            if res.message.tool_calls:
                for tool in res.message.tool_calls:
                    t_name = tool.function.name
                    args = json.loads(tool.function.arguments)
                    args["user_id"] = user_id
                    
                    # Smart Default: If priority is missing, set to medium
                    if t_name == "add_task" and "priority" not in args:
                        args["priority"] = "medium"

                    # Execute the Tool
                    result = await TOOL_FUNCTIONS[t_name](**args)
                    
                    # Second AI Response after tool execution
                    res = self.client.chat(
                        model=self.model,
                        messages=[
                            {"role": "system", "content": SYSTEM_PROMPT},
                            {"role": "user", "content": message},
                            {"role": "assistant", "tool_calls": res.message.tool_calls},
                            {"role": "tool", "tool_call_id": tool.id, "content": json.dumps(result)}
                        ]
                    )

            # Final Text Output
            final_text = res.message.content[0].text if res.message.content else "Processing complete."
            yield json.dumps({"type": "content", "content": final_text, "conversation_id": conversation_id or "default"})
            yield json.dumps({"type": "done"})

        except Exception as e:
            yield json.dumps({"type": "error", "error": f"Agent Error: {str(e)}"})