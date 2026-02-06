from datetime import datetime
from sqlmodel import SQLModel, Field
from typing import Optional
import uuid


def generate_uuid() -> str:
    """Generate a UUID string."""
    return str(uuid.uuid4())


class ConversationBase(SQLModel):
    """Base conversation model with shared fields."""
    user_id: str = Field(max_length=100, index=True)
    title: Optional[str] = Field(default=None, max_length=255)


class Conversation(ConversationBase, table=True):
    """Conversation database model."""
    __tablename__ = "conversations"

    id: str = Field(default_factory=generate_uuid, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class ConversationCreate(SQLModel):
    """Schema for creating a conversation."""
    user_id: str
    title: Optional[str] = None


class ConversationResponse(ConversationBase):
    """Schema for conversation response."""
    id: str
    created_at: datetime
    updated_at: datetime
