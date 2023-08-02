from pydantic import BaseModel


class HiraganaScoreBase(BaseModel):
    score: str


class HiraganaScoreBoardCreate(HiraganaScoreBase):
    pass


class HiraganaScore(HiraganaScoreBase):
    id: int

    class Config:
        from_attributes = True


class KatakanaScoreBase(BaseModel):
    score: str


class KatakanaScoreBoardCreate(KatakanaScoreBase):
    pass


class KatakanaScore(KatakanaScoreBase):
    id: int

    class Config:
        from_attributes = True


class ScoreData(BaseModel):
    hiragana: dict
    katakana: dict

    class Config:
        from_attributes = True


class AnswerRes(BaseModel):
    character: str
    quiz_type: str
