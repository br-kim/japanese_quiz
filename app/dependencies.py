from fastapi import HTTPException, Request


async def check_user(request: Request):
    if not request.session.get('user_id'):
        raise HTTPException(status_code=401, detail="Unauthorized")
