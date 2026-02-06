"""Chat endpoint for AI-powered task management."""
import json
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Any

router = APIRouter(prefix="/api", tags=["chat"])


class ChatRequest(BaseModel):
    """Request schema for chat endpoint."""
    message: str
    conversation_id: Optional[str] = None
    user_id: str = "default"


class ChatResponse(BaseModel):
    """Response schema for chat endpoint."""
    success: bool
    conversation_id: Optional[str] = None
    response: Optional[str] = None
    tool_calls: List[Any] = []
    error: Optional[str] = None


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Process a chat message through the AI agent.
    Returns a simple JSON response (non-streaming for debugging).
    """
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    # Import here to catch initialization errors
    try:
        from app.services.agent import TodoAgent
    except Exception as e:
        return ChatResponse(
            success=False,
            error=f"Failed to import agent: {str(e)}"
        )

    try:
        agent = TodoAgent()
    except Exception as e:
        return ChatResponse(
            success=False,
            error=f"Failed to initialize agent: {str(e)}"
        )

    # Collect all responses from the generator
    responses = []
    tool_calls = []
    final_content = ""
    conversation_id = None

    try:
        async for chunk in agent.chat(
            message=request.message,
            conversation_id=request.conversation_id,
            user_id=request.user_id,
        ):
            try:
                data = json.loads(chunk)
                responses.append(data)

                if data.get("type") == "content":
                    final_content = data.get("content", "")
                    conversation_id = data.get("conversation_id")
                elif data.get("type") == "tool_call":
                    tool_calls.append({
                        "tool": data.get("tool"),
                        "arguments": data.get("arguments")
                    })
                    conversation_id = data.get("conversation_id")
                elif data.get("type") == "tool_result":
                    tool_calls.append({
                        "tool": data.get("tool"),
                        "result": data.get("result")
                    })
                elif data.get("type") == "error":
                    return ChatResponse(
                        success=False,
                        conversation_id=data.get("conversation_id"),
                        error=data.get("error"),
                        tool_calls=tool_calls
                    )
                elif data.get("type") == "done":
                    conversation_id = data.get("conversation_id")

            except json.JSONDecodeError:
                continue

        return ChatResponse(
            success=True,
            conversation_id=conversation_id,
            response=final_content,
            tool_calls=tool_calls
        )

    except Exception as e:
        return ChatResponse(
            success=False,
            conversation_id=conversation_id,
            error=f"Chat processing error: {str(e)}",
            tool_calls=tool_calls
        )
