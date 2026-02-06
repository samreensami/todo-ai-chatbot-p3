from datetime import datetime
from sqlmodel import SQLModel, Field
from typing import Optional


class MessageBase(SQLModel):
    """Base message model with shared fields."""
    conversation_id: str = Field(foreign_key="conversations.id", index=True)
    role: str = Field(max_length=20)  # user, assistant, tool
    content: str
    tool_calls: Optional[str] = Field(default=None)  # JSON serialized


class Message(MessageBase, table=True):
    """Message database model."""
    __tablename__ = "messages"

    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class MessageCreate(SQLModel):
    """Schema for creating a message."""
    conversation_id: str
    role: str
    content: str
    tool_calls: Optional[str] = None


class MessageResponse(MessageBase):
    """Schema for message response."""
    id: int
    created_at: datetime
