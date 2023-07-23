import urllib.parse
import hashlib
import os

import requests
import jwt
from fastapi import APIRouter, Request, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

import osenv
import urls
import schemas
import crud
from dependencies import get_db
from utils import create_token

login_router = APIRouter()
templates = Jinja2Templates(directory='templates')


@login_router.get("/login")
async def login(request: Request):
    """
    로그인 URL 리턴 API
    """
    base_url = 'https://accounts.google.com/o/oauth2/v2/auth?'
    url_dict = {
        'response_type': 'code',
        'scope': " ".join(urls.GOOGLE_AUTH_SCOPES),
        'access_type': 'offline',
        'include_granted_scopes': 'true',
        'redirect_uri': f'{request.base_url}',
        'client_id': osenv.GOOGLE_CLIENT_ID,
    }
    req_url = base_url + urllib.parse.urlencode(url_dict)
    return req_url

@login_router.get("/oauth")
async def google_oauth(request: Request, code, db: Session = Depends(get_db)):
    """
    구글 OAuth 인증 API
    """
    params = {
        "code": code,
        "client_id": osenv.GOOGLE_CLIENT_ID,
        "client_secret": osenv.GOOGLE_CLIENT_SECRET,
        "redirect_uri": f"{request.base_url}",
        "grant_type": "authorization_code",
    }
    res = requests.post(urls.GOOGLE_GET_TOKEN_URL, data=params)
    response_json = res.json()
    if res.status_code != 200:
        # 구글 인증 에러
        raise HTTPException(status_code=400)
    id_token = response_json.get("id_token")
    res_info = jwt.decode(id_token, options={"verify_signature": False})
    user_email = res_info.get("email")
    user_name = res_info.get("given_name")
    email = schemas.UserCreate(email=user_email)
    db_user = crud.get_user_by_email(db=db, email=user_email)
    if db_user:
        if not crud.get_user_hiragana_score(db=db, user_id=db_user.id):
            crud.create_user_scoreboard(db=db, user_id=db_user.id)
    else:
        db_user = crud.create_user(db=db, user=email)
        crud.create_user_scoreboard(db=db, user_id=db_user.id)

    payload = dict(user_email=user_email, user_name=user_name, user_id=db_user.id)
    token = create_token(payload=payload)
    return token


@login_router.get("/logout")
async def logout(request: Request):
    """
    로그아웃 API
    """
    token = None
    token_revoke = f"https://oauth2.googleapis.com/revoke?token={token}"
    header = {
        "Content-type": "application/x-www-form-urlencoded"
    }
    requests.post(token_revoke, headers=header)
    request.get('https://mail.google.com/mail/u/0/?logout&hl=en')
    return templates.TemplateResponse("error.html", {"request": request, "message": "로그아웃이 완료되었습니다."})
