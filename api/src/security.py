from fastapi import Security, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from src import config


_security = HTTPBearer()


def verify_token(credentials: HTTPAuthorizationCredentials = Security(_security)) -> str:
    if credentials.credentials != config.TEST_ACCESS_TOKEN:
        raise HTTPException(status_code=403, detail="Invalid or missing token")
    return credentials.credentials
