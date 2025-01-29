from pydantic import BaseModel


class BookCreate(BaseModel):
    title: str
    description: str
    publication_date: str  # ISO format
    genre: str
    available_copies: int


class BookUpdate(BookCreate):
    pass


class BookOut(BaseModel):
    id: int
    title: str
    description: str
    publication_date: str
    genre: str
    available_copies: int
