from collections.abc import Callable

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError
from sqlalchemy.orm import Session

from auth.security import decode_access_token
from database import get_db
from models import Annotation, Catalog, User, Video

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_access_token(token)
        user_id_raw = payload.get("sub") or payload.get("user_id")
        if user_id_raw is None:
            raise credentials_exception
        user_id = int(user_id_raw)
    except (PyJWTError, ValueError, TypeError):
        raise credentials_exception

    user = db.get(User, user_id)
    if user is None:
        raise credentials_exception
    return user


def require_role(*allowed_roles: str) -> Callable[[User], User]:
    def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Forbidden: Insufficient role permissions",
            )
        return current_user

    return role_checker


def get_owned_catalog(
    catalog_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Catalog:
    catalog = db.get(Catalog, catalog_id)
    if catalog is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Catalog with id {catalog_id} not found",
        )

    if current_user.role != "admin" and catalog.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden: You do not own this catalog",
        )
    return catalog


def get_owned_annotation(
    catalog_id: int,
    video_id: int,
    annotation_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Annotation:
    catalog = db.get(Catalog, catalog_id)
    if catalog is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Catalog with id {catalog_id} not found",
        )

    video = db.get(Video, video_id)
    if video is None or video.catalog_id != catalog_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Video with id {video_id} not found in catalog {catalog_id}",
        )

    annotation = db.get(Annotation, annotation_id)
    if annotation is None or annotation.video_id != video_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Annotation with id {annotation_id} not found for video {video_id}",
        )

    if current_user.role != "admin" and annotation.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden: You do not own this annotation",
        )
    return annotation
