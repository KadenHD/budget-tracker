from datetime import timezone, datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from app.schemas.auth import Settings
from pwdlib import PasswordHash
from typing import Optional
import jwt

settings = Settings()
password_hasher = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

EXPIRED = "EXPIRED"

def hash_password(password: str) -> str:
    """Hash a plain password."""
    return password_hasher.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Compare a plain password with a hashed one."""
    return password_hasher.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token."""
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.access_token_expire_minutes,
        )

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        settings.secret_key.get_secret_value(),
        algorithm=settings.algorithm,
    )

    return encoded_jwt

def verify_access_token(token: str, expected_type: str) -> Optional[str]:
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
        data={"sub": user_id, "type": "email_verification"},
        expires_delta=timedelta(hours=24),
    )
