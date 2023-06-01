from datetime import datetime, timedelta
from typing import Optional

from pydantic import BaseModel


class ActiveGameCreate(BaseModel):
    game_id: str


class ActiveGameOut(BaseModel):
    game_id: int
    generated_code: int
    total_gamers: int
    is_active: bool

    class Config:
        orm_mode = True


class ActiveGamerCreate(BaseModel):
    generated_code: int
    username: str
    image: str


class ActiveGamersOut(BaseModel):
    username: str
    image: str
    points: int

    class Config:
        orm_mode = True
