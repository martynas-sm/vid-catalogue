from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from schemas.common import PaginationMeta


class UserBase(BaseModel):
    username: str = Field(
        ...,
        min_length=3,
        max_length=50,
        description="Unique username",
        examples=["adomas"],
    )
    email: EmailStr = Field(
        ...,
        description="Unique email address",
        examples=["adomas@example.com"],
    )
    role: Literal["guest", "member", "admin"] = Field(
        default="member",
        description="User role ('guest', 'member', 'admin')",
        examples=["admin"],
    )


class UserCreate(UserBase):
    password: str = Field(
        ...,
        min_length=6,
        max_length=100,
        description="User password",
        examples=["secretpassword123"],
    )


class UserUpdate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, examples=["adomas"])
    email: EmailStr = Field(..., examples=["adomas@example.com"])
    role: Literal["guest", "member", "admin"] = Field(
        default="member", examples=["admin"]
    )


class UserResponse(UserBase):
    id: int = Field(..., examples=[1])
    created_at: datetime
    updated_at: datetime
    links: dict[str, str] = Field(
        default_factory=dict,
        description="HATEOAS hypermedia links",
        examples=[{"self": "/users/1"}],
    )

    model_config = ConfigDict(from_attributes=True)


class UserListResponse(BaseModel):
    users: list[UserResponse]
    pagination: PaginationMeta
    links: dict[str, str] = Field(
        default_factory=dict,
        description="HATEOAS pagination links",
        examples=[{"self": "/users?limit=10&offset=0"}],
    )
