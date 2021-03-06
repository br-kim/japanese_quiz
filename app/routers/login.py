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

login_router = APIRouter()
templates = Jinja2Templates(directory='templates')


@login_router.get("/login")
async def login(request: Request):
    state = hashlib.sha256(os.urandom(1024)).hexdigest()
    request.session['state'] = state
    base_url = 'https://accounts.google.com/o/oauth2/v2/auth?'
    url_dict = {
        'response_type': 'code',
        'scope': " ".join(urls.GOOGLE_AUTH_SCOPES),
        'access_type': 'offline',
        'include_granted_scopes': 'true',
        'state': state,
        'redirect_uri': f'{request.base_url}forredirect',
        'client_id': osenv.GOOGLE_CLIENT_ID,
    }
    req_url = base_url + urllib.parse.urlencode(url_dict)
    return RedirectResponse(req_url)


@login_router.get("/forredirect")
async def forredirect(request: Request, db: Session = Depends(get_db)):
    if request.query_params["state"] != request.session["state"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    code = request.query_params["code"]
    params = {
        "code": code,
        "client_id": osenv.GOOGLE_CLIENT_ID,
        "client_secret": osenv.GOOGLE_CLIENT_SECRET,
        'redirect_uri': f'{request.base_url}forredirect',
        "grant_type": "authorization_code",
    }
    res = requests.post(urls.GOOGLE_GET_TOKEN_URL, data=params)
    response_json = res.json()
    id_token = response_json.get('id_token')
    res_info = jwt.decode(id_token, options={"verify_signature": False})
    user_email = res_info.get('email')
    user_name = res_info.get('given_name')
    request.session['user_email'] = user_email
    request.session['user_name'] = user_name
    request.session['user_token'] = response_json['access_token']
    email = schemas.UserCreate(email=user_email)
    db_user = crud.get_user_by_email(db=db, email=user_email)
    if db_user:
        if not crud.get_user_hiragana_score(db=db, user_id=db_user.id):
            crud.create_user_scoreboard(db=db, user_id=db_user.id)
    else:
        current_db_user = crud.create_user(db=db, user=email)
        crud.create_user_scoreboard(db=db, user_id=current_db_user.id)
    return RedirectResponse('/')


@login_router.get("/logout")
async def logout(request: Request):
    token = request.session.get('user_token')
    request.session['user_email'] = None
    request.session['user_name'] = None
    request.session['user_token'] = None
    token_revoke = f"https://oauth2.googleapis.com/revoke?token={token}"
    header = {
        "Content-type": "application/x-www-form-urlencoded"
    }
    requests.post(token_revoke, headers=header)
    request.get('https://mail.google.com/mail/u/0/?logout&hl=en')
    return templates.TemplateResponse("error.html", {"request": request, "message": "??????????????? ?????????????????????."})
