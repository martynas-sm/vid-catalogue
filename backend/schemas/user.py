from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from schemas.common import PaginationMeta


class UserBase(BaseModel):
    username: str = Field(
        ..., min_length=3, max_length=50, description="Unique username"
    )
    email: EmailStr = Field(..., description="Unique email address")
    role: Literal["guest", "member", "admin"] = Field(
        default="member", description="User role ('guest', 'member', 'admin')"
    )


class UserCreate(UserBase):
    password: str = Field(
        ..., min_length=6, max_length=100, description="User password"
    )


class UserUpdate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr = Field(...)
    role: Literal["guest", "member", "admin"] = Field(default="member")


class UserResponse(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime
    links: dict[str, str] = Field(default_factory=dict)

    model_config = ConfigDict(from_attributes=True)


class UserListResponse(BaseModel):
    users: list[UserResponse]
    pagination: PaginationMeta
    links: dict[str, str] = Field(default_factory=dict)
