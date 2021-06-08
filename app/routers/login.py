import urllib.parse
import hashlib
import os

import requests
import jwt
from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse

import osenv
import urls

login_router = APIRouter()


@login_router.get("/login")
async def login(request: Request):
    state = hashlib.sha256(os.urandom(1024)).hexdigest()
    request.session['state'] = state
    scope = "https://www.googleapis.com/auth/userinfo.profile"
    scope2 = "https://www.googleapis.com/auth/userinfo.email"
    print(request.session['state'])
    base_url = 'https://accounts.google.com/o/oauth2/v2/auth?'
    url_dict = {
        'response_type': 'code',
        'scope': scope+" "+scope2,
        'access_type': 'offline',
        'include_granted_scopes': 'true',
        'state': state,
        'redirect_uri': f'{request.base_url}forredirect',
        'client_id': osenv.GOOGLE_CLIENT_ID,
    }
    req_url = base_url + urllib.parse.urlencode(url_dict)
    # url = "https://accounts.google.com/o/oauth2/v2/auth?" \
    #       "response_type=code&" \
    #       f"scope={scope}&" \
    #       "access_type=offline&" \
    #       "include_granted_scopes=true&" \
    #       f"state={state}&" \
    #       "redirect_uri=http%3A//127.0.0.1:8000/forredirect&" \
    #       f"client_id={osenv.GOOGLE_CLIENT_ID}"
    return RedirectResponse(req_url)


@login_router.get("/forredirect")
async def forredirect(request: Request):
    if request.query_params["state"] != request.session["state"]:
        return "error"

    code = request.query_params["code"]  # request.session['code']
    params = {
        "code": code,
        "client_id": osenv.GOOGLE_CLIENT_ID,
        "client_secret": osenv.GOOGLE_CLIENT_SECRET,
        'redirect_uri': f'{request.base_url}forredirect',
        "grant_type": "authorization_code",
    }
    res = requests.post(urls.GOOGLE_GET_TOKEN_URL, data=params)
    print(res.json())
    id_token = res.json()['id_token']
    res_info = jwt.decode(id_token, options={"verify_signature": False})
    print(res_info)
    user_email = res_info['email']
    user_name = res_info['given_name']
    request.session['user_id'] = user_email
    request.session['user_name'] = user_name
    request.session['user_token'] = res.json()['access_token']
    # return f"hello, {user_name}. Your E-Mail ID : {user_email}"
    return RedirectResponse('/')


@login_router.get("/logout")
async def logout(request: Request):
    request.session['user_id'] = None
    request.session['user_name'] = None
    token = request.session['user_token']
    request.session['user_token'] = None
    token_revoke = f"https://oauth2.googleapis.com/revoke?token={token}"
    header = {
        "Content-type": "application/x-www-form-urlencoded"
    }
    requests.post(token_revoke, headers=header)
    return RedirectResponse('/')