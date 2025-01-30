from pydantic import BaseModel
from typing import Optional
from datetime import date


class LendingCreate(BaseModel):
    user_id: int
    book_id: int
    lend_date: date  # Тип date вместо str
    return_date: date  # Тип date вместо str


class LendingOut(BaseModel):
    id: int
    user_id: int
    book_id: int
    lend_date: date  # Тип date вместо str
    return_date: date  # Тип date вместо str
    user: Optional['UserOut'] = None  # Строковая ссылка
    book: Optional['BookOut'] = None  # Строковая ссылка

    class Config:
        orm_mode = True


# Вызываем update_forward_refs() после всех импортов
from .user import UserOut
from .book import BookOut

LendingOut.update_forward_refs()
