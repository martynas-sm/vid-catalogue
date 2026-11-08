"""Authentication and authorization dependencies for FastAPI route protection."""

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
    """Validate Bearer access token and return the authenticated User.

    Raises:
        HTTPException: 401 Unauthorized if token is invalid, expired, malformed,
                       or user does not exist in the database.
    """
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
    """Dependency factory restricting route access to specified user roles.

    Args:
        *allowed_roles: Roles permitted to access the endpoint ('admin', 'creator', 'viewer').

    Returns:
        FastAPI dependency function validating caller's role.

    Raises:
        HTTPException: 403 Forbidden if caller's role is not within allowed_roles.
    """

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
    """Fetch a catalog by ID and verify entity ownership or administrative role.

    Args:
        catalog_id: Primary key of the catalog resource from path parameter.
        current_user: Authenticated caller injected via get_current_user.
        db: Active SQLAlchemy database session.

    Returns:
        Catalog instance if found and authorized.

    Raises:
        HTTPException: 404 Not Found if catalog does not exist.
        HTTPException: 403 Forbidden if caller is not an admin and does not own the catalog.
    """
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
    """Fetch an annotation by ID and verify URL hierarchy and entity ownership.

    Enforces strict hierarchy:
      1. Catalog must exist (404).
      2. Video must exist and belong to the catalog (404).
      3. Annotation must exist and belong to the video (404).
      4. Caller must be an admin or the owner (user_id match) (403).

    Args:
        catalog_id: Catalog ID from path.
        video_id: Video ID from path.
        annotation_id: Annotation ID from path.
        current_user: Authenticated user injected via get_current_user.
        db: Active database session.

    Returns:
        Annotation instance if found, hierarchically valid, and authorized.

    Raises:
        HTTPException: 404 Not Found if catalog, video, or annotation missing or mismatched.
        HTTPException: 403 Forbidden if caller is not an admin and does not own the annotation.
    """
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
