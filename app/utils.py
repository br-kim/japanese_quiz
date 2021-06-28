import os
from typing import Optional


def gen_img_path(gana: str):
    return "./static/img/" + gana


def gen_img_path_list(gana_type: str):
    result = []
    flag = False
    if gana_type == 'all':
        flag = True
    if gana_type == 'hiragana' or flag:
        result += hiragana_urls
    if gana_type == 'katakana' or flag:
        result += katakana_urls
    return result


hiragana_url = gen_img_path('hiragana')
katakana_url = gen_img_path('katakana')

hiragana_urls = [hiragana_url+"/" + i for i in os.listdir(hiragana_url)]
katakana_urls = [katakana_url+"/" + i for i in os.listdir(katakana_url)]

