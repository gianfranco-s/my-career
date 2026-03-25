import jwt

from fastapi import Security, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from my_career.config import auth_settings

bearer = HTTPBearer()


def require_auth(credentials: HTTPAuthorizationCredentials = Security(bearer)) -> None:
    try:
        jwt.decode(
            credentials.credentials,
            auth_settings.jwt_secret.get_secret_value(),
            algorithms=[auth_settings.jwt_algorithm],
            options={"require": ["exp"]},
        )
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
