from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    password: str
    is_admin: bool


class UserOut(BaseModel):
    id: int
    username: str
    is_admin: bool
