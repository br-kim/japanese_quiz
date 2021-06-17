from fastapi import HTTPException, Request

from database import SessionLocal


async def check_user(request: Request):
    if not request.session.get('user_email'):
        raise HTTPException(status_code=401, detail="Unauthorized")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
