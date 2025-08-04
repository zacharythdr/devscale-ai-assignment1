from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from starlette import status

from app.database import Book, get_db_session
from app.schema import BookCreate, BookRead

books_router = APIRouter(prefix="/Books", tags=["Books"])


@books_router.get("/", response_model=list[BookRead])
def get_books(db: Session = Depends(get_db_session)):
    books = db.exec(select(Book)).all()
    return books


@books_router.get("/{book_id}", response_model=BookRead)
def get_book(book_id: int, db: Session = Depends(get_db_session)):
    book = db.get(Book, book_id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Note not found"
        )
    return book


@books_router.post("/", status_code=status.HTTP_201_CREATED)
def create_book(book: BookCreate, db: Session = Depends(get_db_session)):
    new_book = Book(title=book.title, author=book.author)
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book.model_dump()


@books_router.patch("/{book_id}", response_model=BookRead)
def update_book(book_id: int, book: BookCreate, db: Session = Depends(get_db_session)):
    db_book: Any = db.get(Book, book_id)
    if not db_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book Not Found"
        )

    db_book.title = book.title
    db_book.author = book.author
    db.commit()
    db.refresh(db_book)

    return db_book.model_dump()


@books_router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int, db: Session = Depends(get_db_session)):
    db_book = db.get(Book, book_id)
    if not db_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )

    db.delete(db_book)
    db.commit()
