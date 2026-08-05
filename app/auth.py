import os
from fastapi import Header, HTTPException, status

ADMIN_API_KEY = os.getenv("ADMIN_API_KEY")


def require_admin_key(x_admin_key: str = Header(default=None)) -> None:
    if not ADMIN_API_KEY:
        # Fail closed: if the env var isn't set, refuse all admin writes
        # rather than silently allowing them.
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Admin API key not configured on server.",
        )
    if not x_admin_key or x_admin_key != ADMIN_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid X-Admin-Key header.",
        )
