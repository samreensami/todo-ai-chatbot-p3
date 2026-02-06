"""Conversation management endpoints."""
from fastapi import APIRouter, HTTPException
from sqlmodel import select
from typing import Optional
from datetime import datetime

from app.database import get_db_session
from app.models import Conversation, Message, ConversationResponse, MessageResponse

router = APIRouter(prefix="/api/conversations", tags=["conversations"])


class ConversationWithMessages(ConversationResponse):
    """Conversation with its messages."""
    messages: list[MessageResponse] = []


@router.get("")
async def list_conversations(user_id: str) -> list[ConversationResponse]:
    """List all conversations for a user."""
    async with get_db_session() as session:
        query = (
            select(Conversation)
            .where(Conversation.user_id == user_id)
            .order_by(Conversation.updated_at.desc())
        )
        result = await session.execute(query)
        conversations = result.scalars().all()

        return [
            ConversationResponse(
                id=conv.id,
                user_id=conv.user_id,
                title=conv.title,
                created_at=conv.created_at,
                updated_at=conv.updated_at,
            )
            for conv in conversations
        ]


@router.get("/{conversation_id}")
async def get_conversation(conversation_id: str) -> ConversationWithMessages:
    """Get a conversation with all its messages."""
    async with get_db_session() as session:
        # Get conversation
        query = select(Conversation).where(Conversation.id == conversation_id)
        result = await session.execute(query)
        conversation = result.scalar_one_or_none()

        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")

        # Get messages
        messages_query = (
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at)
        )
        messages_result = await session.execute(messages_query)
        messages = messages_result.scalars().all()

        return ConversationWithMessages(
            id=conversation.id,
            user_id=conversation.user_id,
            title=conversation.title,
            created_at=conversation.created_at,
            updated_at=conversation.updated_at,
            messages=[
                MessageResponse(
                    id=msg.id,
                    conversation_id=msg.conversation_id,
                    role=msg.role,
                    content=msg.content,
                    tool_calls=msg.tool_calls,
                    created_at=msg.created_at,
                )
                for msg in messages
            ],
        )


@router.delete("/{conversation_id}")
async def delete_conversation(conversation_id: str) -> dict:
    """Delete a conversation and all its messages."""
    async with get_db_session() as session:
        # Get conversation
        query = select(Conversation).where(Conversation.id == conversation_id)
        result = await session.execute(query)
        conversation = result.scalar_one_or_none()

        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")

        # Delete messages first (cascade would handle this, but being explicit)
        messages_query = select(Message).where(Message.conversation_id == conversation_id)
        messages_result = await session.execute(messages_query)
        messages = messages_result.scalars().all()

        for msg in messages:
            await session.delete(msg)

        # Delete conversation
        await session.delete(conversation)
        await session.commit()

        return {
            "success": True,
            "message": f"Conversation {conversation_id} deleted",
        }
