import os
import urllib.parse
import hashlib

import uvicorn
import requests
import jwt
from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.staticfiles import StaticFiles  # aiofiles import
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from fastapi.middleware.sessions import SessionMiddleware

import urls
import osenv
from routers import quiz

app = FastAPI()
app.mount("/static", StaticFiles(directory='static'), name="static")
templates = Jinja2Templates(directory='templates')
app.include_router(quiz.router)
app.add_middleware(SessionMiddleware, secret_key=osenv.SESSION_KEY)


@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/login")
async def login(request: Request):
    state = hashlib.sha256(os.urandom(1024)).hexdigest()
    request.session['state'] = state
    scope = "https://www.googleapis.com/auth/userinfo.profile"
    print(request.session['state'])
    base_url = 'https://accounts.google.com/o/oauth2/v2/auth?'
    url_dict = {
        'response_type': 'code',
        'scope': scope,
        'access_type': 'offline',
        'include_granted_scopes': 'true',
        'state': state,
        'redirect_uri': 'http://127.0.0.1:8000/forredirect',
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


@app.get("/forredirect")
async def forredirect(request: Request):
    if request.query_params["state"] != request.session["state"]:
        return "error"

    code = request.query_params["code"]  # request.session['code']
    params = {
        "code": code,
        "client_id": osenv.GOOGLE_CLIENT_ID,
        "client_secret": osenv.GOOGLE_CLIENT_SECRET,
        "redirect_uri": "http://127.0.0.1:8000/forredirect",
        "grant_type": "authorization_code",
    }
    res = requests.post(urls.GOOGLE_GET_TOKEN_URL, data=params)
    id_token = res.json()['id_token']
    res_info = jwt.decode(id_token, options={"verify_signature": False})

    user_email = res_info['email']
    user_name = res_info['given_name']
    print(res_info)
    request.session['user_id'] = user_email
    request.session['user_name'] = user_name
    # return f"hello, {user_name}. Your E-Mail ID : {user_email}"
    return RedirectResponse('/')

if __name__ == "__main__":
    uvicorn.run("apps:app", host="0.0.0.0", port=osenv.PORT_NUMBER)
