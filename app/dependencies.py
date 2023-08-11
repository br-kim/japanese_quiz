from fastapi import Request, HTTPException, Depends, Query
from fastapi.security import HTTPBearer

from database import SessionLocal
from utils.utils import get_token_payload
from crud import get_user_by_email


authorization = HTTPBearer()

def get_db():
    db = SessionLocal()
    db.begin()
    try:
        yield db
    finally:
        db.close()

async def check_user(request: Request, header=Depends(authorization)):
    token = header.credentials
    payload = get_token_payload(token)
    request.state.user_token = payload
    if not payload:
        raise HTTPException(status_code=403)
    return payload

async def check_admin(request: Request, db=Depends(get_db), header=Depends(authorization)):
    token = header.credentials
    payload = get_token_payload(token)
    request.state.user_token = payload
    user = get_user_by_email(db, payload.get("user_email"))
    if not payload or user.permission != 1:
        raise HTTPException(status_code=404)
    return payload

async def check_user_by_query(token=Query(..., alias="token")):
    payload = get_token_payload(token)
    if not payload:
        raise HTTPException(status_code=403)
    return payload

async def check_user_optional_token(request: Request):
    token = request.headers.get("Authorization")
    if not token:
        return None

    if token.startswith("Bearer "):
        token = token.split(" ")[1]
    try:
        payload = get_token_payload(token)
        request.state.user_token = payload
    except Exception as e:
        return None
    return payload


