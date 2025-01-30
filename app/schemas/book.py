from pydantic import BaseModel
from typing import List, Optional
from datetime import date


class BookCreate(BaseModel):
    title: str
    description: str
    publication_date: date  # Тип date вместо str
    genre: str
    available_copies: int
    author_ids: List[int]


class BookUpdate(BookCreate):
    pass


class BookOut(BaseModel):
    id: int
    title: str
    description: str
    publication_date: date  # Тип date вместо str
    genre: str
    available_copies: int
    authors: List['AuthorOut'] = []  # Строковая ссылка
    lendings: List['LendingOut'] = []  # Строковая ссылка

    class Config:
        orm_mode = True


# Вызываем update_forward_refs() после всех импортов
from .author import AuthorOut
from .lending import LendingOut

BookOut.update_forward_refs()
