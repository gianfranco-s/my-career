import jwt

from fastapi import Security, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from my_career.config import JWT_SECRET, JWT_ALGORITHM

bearer = HTTPBearer()


def require_auth(credentials: HTTPAuthorizationCredentials = Security(bearer)) -> None:
    try:
        jwt.decode(
            credentials.credentials,
            JWT_SECRET,
            algorithms=[JWT_ALGORITHM],
            options={"require": ["exp"]},
        )
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
