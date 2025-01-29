from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas, models
from app.database import get_db
from app.utils.auth import get_current_user, get_admin_user

router = APIRouter()


@router.post("/books/", response_model=schemas.BookOut)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db),
                current_user: models.User = Depends(get_admin_user)):
    return crud.create_book(db=db, book=book)


@router.get("/books/", response_model=list[schemas.BookOut])
def read_books(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    books = crud.get_books(db, skip=skip, limit=limit)
    return books


@router.get("/books/{book_id}", response_model=schemas.BookOut)
def read_book(book_id: int, db: Session = Depends(get_db)):
    db_book = crud.get_book(db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book


@router.put("/books/{book_id}", response_model=schemas.BookOut)
def update_book(book_id: int, book: schemas.BookUpdate, db: Session = Depends(get_db),
                current_user: models.User = Depends(get_admin_user)):
    updated_book = crud.update_book(db=db, book_id=book_id, book=book)
    if updated_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return updated_book


@router.delete("/books/{book_id}", response_model=schemas.BookOut)
def delete_book(book_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_admin_user)):
    deleted_book = crud.delete_book(db=db, book_id=book_id)
    if deleted_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return deleted_book
