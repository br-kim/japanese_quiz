from pydantic import BaseModel


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int

    class Config:
        orm_mode = True


class HiraganaScoreBase(BaseModel):
    score: str


class HiraganaScoreBoardCreate(HiraganaScoreBase):
    pass


class HiraganaScore(HiraganaScoreBase):
    id: int

    class Config:
        orm_mode = True


class KatakanaScoreBase(BaseModel):
    score: str


class KatakanaScoreBoardCreate(KatakanaScoreBase):
    pass


class KatakanaScore(KatakanaScoreBase):
    id: int

    class Config:
        orm_mode = True
