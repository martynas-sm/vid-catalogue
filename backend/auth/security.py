import secrets
from datetime import datetime, timedelta, timezone
from typing import Any

import jwt
from pwdlib import PasswordHash
from pwdlib.exceptions import UnknownHashError

from auth.config import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY

# Initialize recommended Argon2id password hasher
password_hash = PasswordHash.recommended()

# Precompute dummy hash at module load time to mitigate timing attacks on username enumeration.
# Precomputing ensures that verifying against DUMMY_HASH incurs only verification time (~50-80ms),
# exactly mirroring the execution path of an existing user.
DUMMY_HASH: str = password_hash.hash("dummypassword")


def hash_password(password: str) -> str:
    """Hash a plaintext password using Argon2id.

    Args:
        password: The plaintext password to hash.

    Returns:
        The Argon2id hash string.
    """
    return password_hash.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plaintext password against an Argon2id hash.

    Args:
        plain_password: The candidate plaintext password.
        hashed_password: The stored Argon2id hash string.

    Returns:
        True if the password matches the hash, False otherwise.
    """
    try:
        return password_hash.verify(plain_password, hashed_password)
    except (UnknownHashError, ValueError, TypeError):
        return False


def verify_dummy_password(password: str = "dummypassword") -> bool:
    """Perform constant-time password verification against precomputed DUMMY_HASH.

    Used when a requested username does not exist in the database, preventing
    timing side-channel attacks for username enumeration.

    Args:
        password: The candidate password to verify (defaults to dummy password).

    Returns:
        bool: Result of dummy verification (always False for wrong password,
              or True if 'dummypassword' is passed; caller should treat user
              as non-existent regardless).
    """
    return verify_password(password, DUMMY_HASH)


def create_access_token(
    user_id: int,
    role: str,
    expires_delta: timedelta | None = None,
) -> str:
    """Create a signed HS256 JWT access token.

    Args:
        user_id: The primary key ID of the user.
        role: The role assigned to the user ('admin', 'creator', 'viewer').
        expires_delta: Optional custom lifespan for the token. If omitted,
                       defaults to ACCESS_TOKEN_EXPIRE_MINUTES.

    Returns:
        Encoded JWT string signed with SECRET_KEY using ALGORITHM.
    """
    now = datetime.now(timezone.utc)
    if expires_delta is not None:
        expire = now + expires_delta
    else:
        expire = now + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    payload: dict[str, Any] = {
        "sub": str(user_id),
        "user_id": user_id,
        "role": role,
        "iat": now,
        "exp": expire,
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> dict[str, Any]:
    """Decode and validate a JWT access token.

    Validates signature, algorithm restriction (HS256), and expiration (exp),
    and requires presence of 'exp' and 'sub' claims.

    Args:
        token: The encoded JWT access token string.

    Returns:
        The decoded payload dictionary.

    Raises:
        jwt.PyJWTError: If token is expired (ExpiredSignatureError),
                        malformed (DecodeError), or invalid (InvalidTokenError).
    """
    return jwt.decode(
        token,
        SECRET_KEY,
        algorithms=[ALGORITHM],
        options={"require": ["exp", "sub"]},
    )


def create_refresh_token() -> str:
    """Generate a cryptographically secure, high-entropy opaque refresh token.

    Generates 32 bytes of secure random data encoded as URL-safe base64
    (43 characters long, ~256 bits of entropy).

    Returns:
        A unique, cryptographically random string.
    """
    return secrets.token_urlsafe(32)
