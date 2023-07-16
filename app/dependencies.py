from fastapi import Request, HTTPException, Depends
from fastapi.security import HTTPBearer

from database import SessionLocal
from utils import get_token_payload


authorization = HTTPBearer()
async def check_user(request: Request, header=Depends(authorization)):
    token = header.credentials
    payload = get_token_payload(token)
    request.state.user_token = payload
    if not payload:
        raise HTTPException(status_code=403)
    return payload

async def check_user_optional_token(request: Request):
    token = request.headers.get("Authorization")
    if token.startswith("Bearer "):
        token = token.split(" ")[1]
    try:
        payload = get_token_payload(token)
        request.state.user_token = payload
    except Exception as e:
        return None
    return payload


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
