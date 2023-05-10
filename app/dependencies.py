from fastapi import Request

from database import SessionLocal
from utils import get_token_payload


async def check_user(request: Request):
    token = request.headers.get("Authorization")
    payload = get_token_payload(token)
    return payload

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
