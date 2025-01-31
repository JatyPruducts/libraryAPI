from pydantic import BaseModel
from typing import List, Optional
from datetime import date


class UserCreate(BaseModel):
    username: str
    password: str
    is_admin: bool


class UserOut(BaseModel):
    id: int
    username: str
    is_admin: bool
    lendings: List['LendingOut'] = []  # Строковая ссылка

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


# Вызываем update_forward_refs() после всех импортов
from .lending import LendingOut
UserOut.update_forward_refs()
