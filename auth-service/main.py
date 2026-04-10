import os
from contextlib import asynccontextmanager
from datetime import datetime, timezone, timedelta

import bcrypt
import jwt
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm

JWT_SECRET = os.environ.get("JWT_SECRET", "")
JWT_ALGORITHM = "HS256"
JWT_TTL_HOURS = int(os.environ.get("JWT_TTL_HOURS", "24"))
USERS = os.environ.get("USERS", "")


def _load_users(raw_users: str) -> dict[str, bytes]:
    # Users are defined via env var: USERS=alice:plaintextpw,bob:plaintextpw
    if not raw_users:
        return {}
    result = {}
    for entry in raw_users.split(","):
        username, password = entry.split(":")
        result[username.strip()] = bcrypt.hashpw(password.strip().encode(), bcrypt.gensalt())
    return result


@asynccontextmanager
async def lifespan(app: FastAPI):
    if not JWT_SECRET:
        raise RuntimeError("JWT_SECRET env var is not set")
    if not USERS:
        raise RuntimeError("USERS env var is not set")
    app.state.users = _load_users(USERS)
    yield


app = FastAPI(title="Auth Service", lifespan=lifespan)


@app.post("/v1/auth/token")
async def login(request: Request, form: OAuth2PasswordRequestForm = Depends()):
    """Issue a JWT bearer token for valid credentials.

    Accepts an OAuth2 password grant form (``application/x-www-form-urlencoded``)
    and returns a signed JWT on success.

    Raises 401 if the username is unknown or the password does not match.

    Note: valid users and their plain-text passwords are loaded at startup from
    the ``USERS`` environment variable (e.g. ``USERS=alice:pass1,bob:pass2``).
    There is currently no user store — credentials live entirely in the environment.
    """
    existing_users: dict = request.app.state.users
    hashed = existing_users.get(form.username)
    if not hashed or not bcrypt.checkpw(form.password.encode(), hashed):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    expires = datetime.now(timezone.utc) + timedelta(hours=JWT_TTL_HOURS)
    payload = {
        "sub": form.username,
        "exp": expires,
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return {"access_token": token, "token_type": "bearer", "expires": expires}
