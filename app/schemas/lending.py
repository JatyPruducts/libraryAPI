from pydantic import BaseModel


class LendingCreate(BaseModel):
    book_id: int
    lend_date: str  # ISO format
    return_date: str  # ISO format


class LendingOut(BaseModel):
    id: int
    user_id: int
    book_id: int
    lend_date: str
    return_date: str
