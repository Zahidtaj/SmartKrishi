"""Password hashing and signed token helpers for local development Admin authentication."""

import base64
import hashlib
import hmac
import json
import secrets
import time
from typing import Any
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from backend.config import get_settings
from backend.database import get_db
from backend.models import AdminUser

bearer_scheme = HTTPBearer(auto_error=False)
PBKDF2_ITERATIONS = 310_000


def hash_password(password: str) -> str:
    """Hash a password using PBKDF2-HMAC-SHA256 with a 16-byte random salt."""
    salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, PBKDF2_ITERATIONS)
    return (
        f"pbkdf2_sha256${PBKDF2_ITERATIONS}$"
        f"{base64.urlsafe_b64encode(salt).decode('ascii')}$"
        f"{base64.urlsafe_b64encode(digest).decode('ascii')}"
    )


def verify_password(password: str, stored_hash: str) -> bool:
    """Constant-time verification against a stored PBKDF2-HMAC-SHA256 hash."""
    try:
        algorithm, iter_str, salt_b64, digest_b64 = stored_hash.split("$", 3)
        if algorithm != "pbkdf2_sha256":
            return False
        iterations = int(iter_str)
        salt = base64.urlsafe_b64decode(salt_b64.encode("ascii"))
        expected_digest = base64.urlsafe_b64decode(digest_b64.encode("ascii"))
        actual_digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations)
        return hmac.compare_digest(actual_digest, expected_digest)
    except Exception:
        return False


def create_access_token(username: str, role: str) -> str:
    """Create an HMAC-SHA256 signed bearer token with expiration."""
    settings = get_settings()
    payload = {
        "sub": username,
        "role": role,
        "exp": int(time.time()) + settings.token_ttl_seconds,
    }
    payload_b64 = base64.urlsafe_b64encode(json.dumps(payload, separators=(",", ":")).encode("utf-8")).decode("ascii")
    sig = hmac.new(settings.token_secret.encode("utf-8"), payload_b64.encode("ascii"), hashlib.sha256).digest()
    sig_b64 = base64.urlsafe_b64encode(sig).decode("ascii")
    return f"{payload_b64}.{sig_b64}"


def decode_access_token(token: str) -> dict[str, Any]:
    """Verify token signature and expiry; raise HTTP 401 on any mismatch."""
    settings = get_settings()
    try:
        payload_b64, sig_b64 = token.split(".", 1)
        expected_sig = hmac.new(
            settings.token_secret.encode("utf-8"),
            payload_b64.encode("ascii"),
            hashlib.sha256,
        ).digest()
        provided_sig = base64.urlsafe_b64decode(sig_b64.encode("ascii"))
        if not hmac.compare_digest(expected_sig, provided_sig):
            raise ValueError("Invalid token signature")
        payload = json.loads(base64.urlsafe_b64decode(payload_b64.encode("ascii")).decode("utf-8"))
        if int(payload.get("exp", 0)) < int(time.time()):
            raise ValueError("Token expired")
        return payload
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication credentials are invalid or expired.",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc


def require_admin(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> AdminUser:
    """FastAPI dependency enforcing authenticated, active Admin access."""
    if credentials is None or not credentials.credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Administrator authentication is required.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    payload = decode_access_token(credentials.credentials)
    username = payload.get("sub")
    if not username or payload.get("role") != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions.")

    admin_user = db.query(AdminUser).filter(AdminUser.username == username, AdminUser.is_active.is_(True)).first()
    if admin_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Administrator account not found or inactive.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return admin_user
