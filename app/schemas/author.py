from pydantic import BaseModel
from typing import List
from datetime import date


class AuthorCreate(BaseModel):
    name: str
    biography: str
    date_of_birth: date  # Тип date вместо str


class AuthorUpdate(AuthorCreate):
    pass


class AuthorOut(BaseModel):
    id: int
    name: str
    biography: str
    date_of_birth: date  # Тип date вместо str
    books: List['BookOut'] = []  # Строковая ссылка

    class Config:
        orm_mode = True


# Вызываем update_forward_refs() после всех импортов
from .book import BookOut

AuthorOut.update_forward_refs()
