from pydantic import BaseModel


class AuthorCreate(BaseModel):
    name: str
    biography: str
    date_of_birth: str  # ISO format


class AuthorUpdate(AuthorCreate):
    pass


class AuthorOut(BaseModel):
    id: int
    name: str
    biography: str
    date_of_birth: str
