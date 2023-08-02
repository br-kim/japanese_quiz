import os
from functools import lru_cache

from pydantic_settings import BaseSettings

class TestSettings(BaseSettings):
    DATABASE_URL: str = os.getenv('DATABASE_URL', default="postgresql://ii:1234@localhost:5432/test_database")
    SERVER_URL: str = "http://localhost:8000"


class LocalSettings(BaseSettings):
    DATABASE_URL: str = os.getenv('DATABASE_URL', default="postgresql://ii:1234@localhost:5432/japanese_quiz")
    SERVER_URL: str = "http://localhost:8000"


class ProductionSettings(BaseSettings):
    DATABASE_URL: str = os.getenv('DATABASE_URL', default="postgresql://ii:1234@localhost:5432/japanese_quiz")
    SERVER_URL: str = "https://japanese-quiz.site"


@lru_cache()
def get_settings():
    environ = os.getenv('JPN_QUIZ_ENVIRON', "test")
    if environ == "test":
        return TestSettings()
    elif environ == "local":
        return LocalSettings()
    elif environ == "prod":
        return ProductionSettings()
