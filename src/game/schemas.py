from datetime import datetime, timedelta
from typing import Optional

from pydantic import BaseModel


class GameCreate(BaseModel):
    title: str
    description: Optional[str] = None
    cover_image: str
    type: str


class GameAllCreate(BaseModel):
    title: str
    description: Optional[str] = None
    cover_image: str
    type: str
    questions: list[dict]


class GameOut(GameCreate):
    id: int
    created_at: datetime
    owner_id: int

    class Config:
        orm_mode = True


class QuestionCreate(BaseModel):
    title: str
    game_id: int
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    time: int
    correct_option: str


class QuestionOut(QuestionCreate):
    class Config:
        orm_mode = True
