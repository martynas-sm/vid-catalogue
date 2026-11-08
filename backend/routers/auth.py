"""Authentication router providing registration, login, token refresh, logout, and 2FA."""

from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from auth.config import REFRESH_TOKEN_EXPIRE_DAYS
from auth.dependencies import get_current_user
from auth.security import (
    create_access_token,
    create_refresh_token,
    decode_access_token,
    hash_password,
    verify_dummy_password,
    verify_password,
)
from auth.totp import (
    generate_totp_secret,
    get_provisioning_uri,
    verify_totp_code,
)
from database import get_db
from models import RefreshToken, User
from schemas.auth import (
    TokenRefreshRequest,
    TokenRefreshResponse,
    TokenResponse,
    TOTPSetupResponse,
    TOTPVerifyRequest,
    UserLoginRequest,
    UserRegisterRequest,
)
from schemas.user import UserResponse

router = APIRouter()


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user account",
    responses={
        400: {"description": "Username or email already registered"},
    },
)
def register(
    payload: UserRegisterRequest,
    db: Session = Depends(get_db),
):
    if db.query(User).filter(User.username == payload.username).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )
    if db.query(User).filter(User.email == payload.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    new_user = User(
        username=payload.username,
        email=payload.email,
        hashed_password=hash_password(payload.password),
        role="creator",
        is_totp_enabled=False,
    )
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already registered",
        )

    return UserResponse(
        id=new_user.id,
        username=new_user.username,
        email=new_user.email,
        role=new_user.role,
        created_at=new_user.created_at,
        updated_at=new_user.updated_at,
        links={"self": f"/users/{new_user.id}"},
    )


@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    summary="Authenticate user and issue access and refresh tokens",
    responses={
        401: {"description": "Invalid credentials or missing/invalid 2FA code"},
    },
)
def login(
    payload: UserLoginRequest,
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.username == payload.username).first()
    if user is None:
        verify_dummy_password()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not verify_password(payload.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if user.is_totp_enabled:
        if not payload.totp_code or not verify_totp_code(
            user.totp_secret, payload.totp_code
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or missing 2FA code",
                headers={"WWW-Authenticate": "Bearer"},
            )

    access_token = create_access_token(user_id=user.id, role=user.role)
    raw_refresh_token = create_refresh_token()
    expires_at = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)

    refresh_record = RefreshToken(
        token=raw_refresh_token,
        user_id=user.id,
        expires_at=expires_at,
        revoked=False,
    )
    db.add(refresh_record)
    db.commit()

    return TokenResponse(
        access_token=access_token,
        refresh_token=raw_refresh_token,
        token_type="bearer",
    )


@router.post(
    "/refresh",
    response_model=TokenRefreshResponse,
    status_code=status.HTTP_200_OK,
    summary="Refresh access token using active refresh token",
    responses={
        401: {"description": "Invalid or expired refresh token"},
    },
)
def refresh(
    payload: TokenRefreshRequest,
    db: Session = Depends(get_db),
):
    token_record = (
        db.query(RefreshToken)
        .filter(RefreshToken.token == payload.refresh_token)
        .first()
    )
    if token_record is None or token_record.revoked:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token_exp = token_record.expires_at
    if token_exp.tzinfo is None:
        token_exp = token_exp.replace(tzinfo=timezone.utc)

    if token_exp <= datetime.now(timezone.utc):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = token_record.user or db.get(User, token_record.user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    new_access_token = create_access_token(user_id=user.id, role=user.role)
    return TokenRefreshResponse(
        access_token=new_access_token,
        token_type="bearer",
    )


@router.post(
    "/logout",
    status_code=status.HTTP_200_OK,
    summary="Revoke refresh token session (logout)",
)
def logout(
    payload: TokenRefreshRequest | None = None,
    authorization: str | None = Header(default=None),
    db: Session = Depends(get_db),
):
    token_to_revoke: str | None = None
    if payload and payload.refresh_token:
        token_to_revoke = payload.refresh_token
    elif authorization and authorization.startswith("Bearer "):
        bearer_val = authorization[7:].strip()
        token_record = (
            db.query(RefreshToken).filter(RefreshToken.token == bearer_val).first()
        )
        if token_record:
            token_record.revoked = True
            db.commit()
            return {"message": "Logged out successfully"}
        try:
            jwt_payload = decode_access_token(bearer_val)
            sub = jwt_payload.get("sub")
            if sub:
                db.query(RefreshToken).filter(
                    RefreshToken.user_id == int(sub),
                    RefreshToken.revoked.is_(False),
                ).update({"revoked": True})
                db.commit()
        except Exception:
            pass
        return {"message": "Logged out successfully"}

    if token_to_revoke:
        token_record = (
            db.query(RefreshToken).filter(RefreshToken.token == token_to_revoke).first()
        )
        if token_record:
            token_record.revoked = True
            db.commit()

    return {"message": "Logged out successfully"}


@router.post(
    "/2fa/setup",
    response_model=TOTPSetupResponse,
    status_code=status.HTTP_200_OK,
    summary="Initialize TOTP 2FA setup for authenticated user",
    responses={
        401: {"description": "Could not validate credentials"},
    },
)
def setup_2fa(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    secret = generate_totp_secret()
    otpauth_uri = get_provisioning_uri(
        username=current_user.username,
        secret=secret,
    )
    current_user.totp_secret = secret
    current_user.is_totp_enabled = False
    db.commit()
    db.refresh(current_user)

    return TOTPSetupResponse(
        secret=secret,
        otpauth_uri=otpauth_uri,
    )


@router.post(
    "/2fa/verify",
    status_code=status.HTTP_200_OK,
    summary="Verify TOTP code and enable 2FA for authenticated user",
    responses={
        400: {"description": "Invalid verification code or setup not initiated"},
        401: {"description": "Could not validate credentials"},
    },
)
def verify_2fa(
    payload: TOTPVerifyRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not current_user.totp_secret:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="2FA setup has not been initiated",
        )

    if not verify_totp_code(
        secret=current_user.totp_secret,
        code=payload.code,
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid verification code",
        )

    current_user.is_totp_enabled = True
    db.commit()
    db.refresh(current_user)

    return {"message": "2FA successfully enabled"}
