import os
import logging
from functools import lru_cache

from pydantic_settings import BaseSettings

from constants import JPN_QUIZ_ENVIRON

class TestSettings(BaseSettings):
    DATABASE_URL: str = os.getenv('DATABASE_URL', default="postgresql://ii:1234@localhost:5432/test_database")
    SERVER_URL: str = "http://localhost:8000"
    DOCS_SETTING: dict = dict(openapi_url = None, docs_url = None, redoc_url = None)
    APP_LOGGING_LEVEL: int = logging.ERROR

class LocalSettings(BaseSettings):
    DATABASE_URL: str = os.getenv('DATABASE_URL', default="postgresql://ii:1234@localhost:5432/japanese_quiz")
    SERVER_URL: str = "http://localhost:8000"
    DOCS_SETTING: dict = dict(openapi_url = "/openapi.json", docs_url = "/docs", redoc_url = "/redoc")
    APP_LOGGING_LEVEL: int = logging.ERROR


class ProductionSettings(BaseSettings):
    DATABASE_URL: str = os.getenv('DATABASE_URL', default="postgresql://ii:1234@localhost:5432/japanese_quiz")
    SERVER_URL: str = "https://japanese-quiz.site"
    DOCS_SETTING: dict = dict(openapi_url = None, docs_url = None, redoc_url = None)
    APP_LOGGING_LEVEL: int = logging.INFO


@lru_cache()
def get_settings():
    if JPN_QUIZ_ENVIRON == "test":
        return TestSettings()
    elif JPN_QUIZ_ENVIRON == "local":
        return LocalSettings()
    elif JPN_QUIZ_ENVIRON == "prod":
        return ProductionSettings()
