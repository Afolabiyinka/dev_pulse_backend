from datetime import datetime, timedelta, timezone
import jwt
from fastapi import HTTPException
from fastapi.security import HTTPBearer
from app.core.config import envVariables

security = HTTPBearer(auto_error=False)

def create_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=envVariables.jwt_expires_mins)
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, envVariables.jwt_secret, algorithm=envVariables.jwt_algorithm)
    return token

def decode_token(token: str) -> dict:
    try:
        payload = jwt.decode(
            token, 
            envVariables.jwt_secret,
            algorithms=[envVariables.jwt_algorithm]
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

