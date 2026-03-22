from datetime import UTC, datetime, timedelta

import jwt
from fastapi.security import OAuth2PasswordBearer
from pwdlib import PasswordHash

from app.schemas.auth import Settings

settings = Settings()
password_hasher = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

EXPIRED = "EXPIRED"
ACCESS_TOKEN="access_token"
EMAIL_VERIFICATION="email_verification"
RESET_TOKEN="reset_token"

def hash_password(password: str) -> str:
    """Hash a plain password."""
    return password_hasher.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Compare a plain password with a hashed one."""
    return password_hasher.verify(plain_password, hashed_password)

def create_access_token(
    subject: str,
    token_type: str = ACCESS_TOKEN,
    expires_delta: timedelta | None = None,
    **extra_claims
) -> str:
    """
    Create a JWT access token.

    Args:
        subject (str): The identifier for the token (e.g., user ID).
        token_type (str, optional): Type of token (default: "access_token").
        expires_delta (Optional[timedelta], optional): Token expiry duration.
        **extra_claims: Additional claims to include in the token.

    Returns:
        str: Encoded JWT token.
    """
    to_encode = {"sub": subject, "type": token_type, **extra_claims}

    expire = datetime.now(UTC) + (
        expires_delta if expires_delta else timedelta(minutes=settings.access_token_expire_minutes)
    )
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        settings.secret_key.get_secret_value(),
        algorithm=settings.algorithm,
    )

    return encoded_jwt

def verify_access_token(token: str, expected_type: str  = ACCESS_TOKEN) -> str | None:
    """Verify a JWT access token and return the subject (user id) if valid and correct type."""
    try:
        payload = jwt.decode(
            token,
            settings.secret_key.get_secret_value(),
            algorithms=[settings.algorithm],
            options={"require": ["exp", "sub"]},
        )
    except jwt.ExpiredSignatureError:
        return EXPIRED
    except jwt.InvalidTokenError:
        return None
    else:
        if payload.get("type") != expected_type:
            return None
        return payload.get("sub")

def create_email_verification_token(user_id: str) -> str:
    return create_access_token(
        subject=str(user_id),
        token_type=EMAIL_VERIFICATION,
        expires_delta=timedelta(hours=24),
    )

def verify_email_verification_token(token: str) -> str | None:
    return verify_access_token(
        token,
        expected_type=EMAIL_VERIFICATION
    )

def create_reset_token(user_id: str) -> str:
    return create_access_token(
        subject=str(user_id),
        token_type=RESET_TOKEN,
        expires_delta=timedelta(hours=1),
    )

def verify_reset_token(token: str) -> str | None:
    return verify_access_token(
        token,
        expected_type=RESET_TOKEN
    )

