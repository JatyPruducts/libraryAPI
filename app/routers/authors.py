from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas, models
from app.database import get_db
from app.utils.auth import get_admin_user

router = APIRouter()


@router.post("/authors/", response_model=schemas.AuthorOut)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db),
                  current_user: models.User = Depends(get_admin_user)):
    return crud.create_author(db=db, author=author)


@router.get("/authors/", response_model=list[schemas.AuthorOut])
def read_authors(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    authors = crud.get_authors(db, skip=skip, limit=limit)
    return authors


@router.get("/authors/{author_id}", response_model=schemas.AuthorOut)
def read_author(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.get_author(db, author_id=author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author


@router.put("/authors/{author_id}", response_model=schemas.AuthorOut)
def update_author(author_id: int, author: schemas.AuthorUpdate, db: Session = Depends(get_db),
                  current_user: models.User = Depends(get_admin_user)):
    updated_author = crud.update_author(db=db, author_id=author_id, author=author)
    if updated_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return updated_author


@router.delete("/authors/{author_id}", response_model=schemas.AuthorOut)
def delete_author(author_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_admin_user)):
    deleted_author = crud.delete_author(db=db, author_id=author_id)
    if deleted_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return deleted_author
