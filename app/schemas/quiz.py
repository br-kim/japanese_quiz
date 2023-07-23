from typing import List

from pydantic import BaseModel


class RandomQuizResponse(BaseModel):
    path: str


class TestQuizResponse(BaseModel):
    order: List[str]