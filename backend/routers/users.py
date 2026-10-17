from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.orm import Session

from database import get_db
from models import User
from schemas.user import (
    UserCreate,
    UserListResponse,
    UserResponse,
    UserUpdate,
)

router = APIRouter()


def make_user_links(user_id: int) -> dict[str, str]:
    return {"self": f"/users/{user_id}"}


@router.get("/users", response_model=UserListResponse)
def get_users(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    username: str | None = None,
    db: Session = Depends(get_db),
):
    query = db.query(User)
    if username:
        query = query.filter(User.username.contains(username))
    total = query.count()
    users = query.offset(offset).limit(limit).all()

    self_url = f"/users?limit={limit}&offset={offset}"
    if username:
        self_url += f"&username={username}"

    return {
        "users": [
            {
                **u.to_dict(),
                "links": make_user_links(u.id),
            }
            for u in users
        ],
        "pagination": {"limit": limit, "offset": offset, "total": total},
        "links": {"self": self_url},
    }


@router.post(
    "/users",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_user(payload: UserCreate, db: Session = Depends(get_db)):
    existing = (
        db.query(User)
        .filter((User.username == payload.username) | (User.email == payload.email))
        .first()
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this username or email already exists",
        )

    user = User(
        username=payload.username,
        email=payload.email,
        hashed_password=f"hashed_{payload.password}",
        role=payload.role,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return {
        **user.to_dict(),
        "links": make_user_links(user.id),
    }


@router.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found",
        )

    return {
        **user.to_dict(),
        "links": make_user_links(user.id),
    }


@router.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, payload: UserUpdate, db: Session = Depends(get_db)):
    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found",
        )

    # Check for duplicate on another user
    conflict = (
        db.query(User)
        .filter(
            (User.id != user_id)
            & ((User.username == payload.username) | (User.email == payload.email))
        )
        .first()
    )
    if conflict:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email is already taken by another user",
        )

    user.username = payload.username
    user.email = payload.email
    user.role = payload.role

    db.commit()
    db.refresh(user)

    return {
        **user.to_dict(),
        "links": make_user_links(user.id),
    }


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found",
        )
    db.delete(user)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
