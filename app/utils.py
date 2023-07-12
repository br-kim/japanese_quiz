import os
from datetime import datetime, timedelta
from typing import Optional

import jwt
from jwt import ExpiredSignatureError
from fastapi import HTTPException

from osenv import JWT_KEY

def gen_img_path(gana: str):
    return "./static/img/" + gana


hiragana_url = gen_img_path('hiragana')
katakana_url = gen_img_path('katakana')

hiragana_urls = [hiragana_url+"/" + i for i in os.listdir(hiragana_url)]
katakana_urls = [katakana_url+"/" + i for i in os.listdir(katakana_url)]


def gen_img_path_list(gana_type: str):
    result = []
    if gana_type == 'hiragana' or gana_type == 'all':
        result += hiragana_urls
    if gana_type == 'katakana' or gana_type == 'all':
        result += katakana_urls
    return result


def create_token(payload:dict):
    # 6시간 후 만료
    exp_timestamp = int((datetime.now()+timedelta(hours=6)).timestamp())
    default_payload = dict(exp=exp_timestamp)
    default_payload.update(payload)
    print(default_payload)
    token = jwt.encode(payload=default_payload, key=JWT_KEY, algorithm="HS256")
    return token


def get_token_payload(token):
    if not token:
        return None
    try:
        payload = jwt.decode(jwt=token.encode(), key=JWT_KEY, algorithms=["HS256"])
    except ExpiredSignatureError:
        raise HTTPException(status_code=403, detail="Token Expire")
    print(payload)
    return payload


if __name__ == "__main__":
    res = create_token(dict())
    print(res)
