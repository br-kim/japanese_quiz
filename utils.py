import os
from typing import Optional


def gen_img_path(gana: str):
    return "./static/img/" + gana


def gen_img_path_list(hiragana: Optional[str], katakana: Optional[str]):
    result = []
    if hiragana:
        result += hiragana_urls
    if katakana:
        result += katakana_urls
    if hiragana is None and katakana is None:
        result += hiragana_urls
        result += katakana_urls
    return result


hiragana_url = gen_img_path('hiragana')
katakana_url = gen_img_path('katakana')

hiragana_urls = [hiragana_url+"/" + i for i in os.listdir(hiragana_url)]
katakana_urls = [katakana_url+"/" + i for i in os.listdir(katakana_url)]

