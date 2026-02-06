from datetime import datetime
from sqlmodel import SQLModel, Field
from typing import Optional
import hashlib


class UserBase(SQLModel):
    """Base user model with shared fields."""
    email: str = Field(unique=True, index=True, max_length=255)
    name: str = Field(max_length=100)


class User(UserBase, table=True):
    """User database model."""
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str = Field(max_length=255)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    @staticmethod
    def hash_password(password: str) -> str:
        """Hash password using SHA-256."""
        return hashlib.sha256(password.encode()).hexdigest()

    def verify_password(self, password: str) -> bool:
        """Verify password against hash."""
        return self.hashed_password == self.hash_password(password)


class UserCreate(SQLModel):
    """Schema for creating a user."""
    email: str
    name: str
    password: str


class UserLogin(SQLModel):
    """Schema for user login."""
    email: str
    password: str


class UserResponse(UserBase):
    """Schema for user response (no password)."""
    id: int
    is_active: bool
    created_at: datetime


class TokenResponse(SQLModel):
    """Schema for token response."""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
