from fastapi import Request, HTTPException

from database import SessionLocal
from utils import get_token_payload


async def check_user(request: Request):
    token = request.headers.get("Authorization")
    print(token)
    payload = get_token_payload(token)
    request.state.user_token = payload
    if not payload:
        raise HTTPException(status_code=403)
    return payload

async def check_user_optional_token(request: Request):
    token = request.headers.get("Authorization")
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
