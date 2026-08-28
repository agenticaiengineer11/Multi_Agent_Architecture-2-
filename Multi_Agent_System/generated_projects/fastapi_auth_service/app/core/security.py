import uuid
from datetime import datetime, timedelta
from typing import Any, Dict, Optional

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.settings import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    """Return a bcrypt hash for the given password."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against its bcrypt hash."""
    return pwd_context.verify(plain_password, hashed_password)


def _create_token(
    data: Dict[str, Any],
    expires_delta: timedelta,
    secret_key: str,
    algorithm: str,
) -> str:
    """Encode a JWT with expiration and issued‑at claims."""
    to_encode = data.copy()
    now = datetime.utcnow()
    expire = now + expires_delta
    to_encode.update({"exp": expire, "iat": now})
    return jwt.encode(to_encode, secret_key, algorithm=algorithm)


def create_access_token(
    subject: str, *, expires_delta: Optional[timedelta] = None
) -> str:
    """
    Create a short‑lived access token.

    Args:
        subject: Identifier for the token owner (e.g., user ID or email).
        expires_delta: Optional custom expiration; defaults to settings value.

    Returns:
        JWT string.
    """
    if expires_delta is None:
        expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "sub": subject,
        "type": "access",
        "jti": str(uuid.uuid4()),
    }
    return _create_token(
        payload,
        expires_delta,
        settings.JWT_SECRET_KEY,
        settings.JWT_ALGORITHM,
    )


def create_refresh_token(
    subject: str, *, expires_delta: Optional[timedelta] = None
) -> str:
    """
    Create a long‑lived refresh token.

    Args:
        subject: Identifier for the token owner.
        expires_delta: Optional custom expiration; defaults to settings value.

    Returns:
        JWT string.
    """
    if expires_delta is None:
        expires_delta = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    payload = {
        "sub": subject,
        "type": "refresh",
        "jti": str(uuid.uuid4()),
    }
    return _create_token(
        payload,
        expires_delta,
        settings.JWT_SECRET_KEY,
        settings.JWT_ALGORITHM,
    )


def decode_token(token: str) -> Dict[str, Any]:
    """
    Decode a JWT and return its payload.

    Raises:
        JWTError: If token is invalid or expired.
    """
    return jwt.decode(
        token,
        settings.JWT_SECRET_KEY,
        algorithms=[settings.JWT_ALGORITHM],
    )


def verify_access_token(token: str) -> Dict[str, Any]:
    """
    Decode and validate an access token.

    Raises:
        JWTError: If token is invalid, expired, or not an access token.
    """
    payload = decode_token(token)
    if payload.get("type") != "access":
        raise JWTError("Invalid token type: expected access token")
    return payload


def verify_refresh_token(token: str) -> Dict[str, Any]:
    """
    Decode and validate a refresh token.

    Raises:
        JWTError: If token is invalid, expired, or not a refresh token.
    """
    payload = decode_token(token)
    if payload.get("type") != "refresh":
        raise JWTError("Invalid token type: expected refresh token")
    return payload


__all__ = [
    "get_password_hash",
    "verify_password",
    "create_access_token",
    "create_refresh_token",
    "decode_token",
    "verify_access_token",
    "verify_refresh_token",
]