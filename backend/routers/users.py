from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from database import get_db
from models import User

router = APIRouter()


@router.get("/users")
async def get_users(
    limit: int = 10,
    offset: int = 0,
    username: str | None = None,
    db: Session = Depends(get_db),
):
    query = db.query(User)
    if username:
        query = query.filter(User.username.contains(username))
    total = query.count()
    users = query.offset(offset).limit(limit).all()

    return {
        "users": [
            {
                "id": u.id,
                "username": u.username,
                "email": u.email,
                "role": u.role,
                "created_at": u.created_at,
                "updated_at": u.updated_at,
                "links": {"self": f"/users/{u.id}"},
            }
            for u in users
        ],
        "pagination": {"limit": limit, "offset": offset, "total": total},
    }


@router.post("/users", status_code=status.HTTP_201_CREATED)
async def create_user(payload: dict = {}, db: Session = Depends(get_db)):
    username = payload.get("username", "user1")
    email = payload.get("email", f"{username}@example.com")

    # Check for uniqueness
    existing = (
        db.query(User)
        .filter((User.username == username) | (User.email == email))
        .first()
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this username or email already exists",
        )

    user = User(
        username=username,
        email=email,
        hashed_password=payload.get("password", "secret123"),
        role=payload.get("role", "member"),
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    result = user.to_dict()
    result.pop("hashed_password", None)
    result["links"] = {"self": f"/users/{user.id}"}
    return {"user": result}


@router.get("/users/{user_id}")
async def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found",
        )

    result = user.to_dict()
    result.pop("hashed_password", None)
    result["links"] = {"self": f"/users/{user.id}"}
    return {"user": result}


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found",
        )
    db.delete(user)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
