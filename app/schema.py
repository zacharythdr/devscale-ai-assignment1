from pydantic import BaseModel


class BookCreate(BaseModel):
    title: str
    author: str


class BookRead(BaseModel):
    id: int
    title: str
    author: str
