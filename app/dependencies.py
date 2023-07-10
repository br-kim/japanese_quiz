from fastapi import Request, HTTPException

from database import SessionLocal
from utils import get_token_payload


async def check_user(request: Request):
    token = request.headers.get("Authorization")
    payload = get_token_payload(token)
    request.state.user_token = payload
    if not payload:
        raise HTTPException(status_code=403)
    return payload

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
