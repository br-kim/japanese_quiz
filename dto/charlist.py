from pydantic import BaseModel


class CharList(BaseModel):
    chars: list