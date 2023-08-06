import os
import logging
from functools import lru_cache

from pydantic_settings import BaseSettings

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
    environ = os.getenv('JPN_QUIZ_ENVIRON', "test")
    if environ == "test":
        return TestSettings()
    elif environ == "local":
        return LocalSettings()
    elif environ == "prod":
        return ProductionSettings()
