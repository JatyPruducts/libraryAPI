from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas, models
from app.database import get_db
from app.utils.auth import get_current_user, get_admin_user

router = APIRouter()


@router.post("/lendings/", response_model=schemas.LendingOut)
def create_lending(lending: schemas.LendingCreate, db: Session = Depends(get_db),
                   current_user: models.User = Depends(get_current_user)):
    # Проверка количества выданных книг у пользователя
    lendings_count = db.query(models.Lending).filter(models.Lending.user_id == current_user.id,
                                                     models.Lending.return_date.is_(None)).count()
    if lendings_count >= 5:
        raise HTTPException(status_code=400, detail="You have reached the maximum number of borrowed books")

    # Проверка наличия книги
    book = db.query(models.Book).filter(models.Book.id == lending.book_id).first()
    if book.available_copies <= 0:
        raise HTTPException(status_code=400, detail="No available copies of this book")

    # Уменьшение количества доступных копий
    book.available_copies -= 1
    db.commit()

    # Создание записи о выдаче
    lending_dict = lending.dict()
    lending_dict['user_id'] = current_user.id
    db_lending = models.Lending(**lending_dict)
    db.add(db_lending)
    db.commit()
    db.refresh(db_lending)
    return db_lending


@router.get("/lendings/", response_model=list[schemas.LendingOut])
def read_lendings(skip: int = 0, limit: int = 10, db: Session = Depends(get_db),
                  current_user: models.User = Depends(get_current_user)):
    if current_user.is_admin:
        lendings = db.query(models.Lending).offset(skip).limit(limit).all()
    else:
        lendings = db.query(models.Lending).filter(models.Lending.user_id == current_user.id).offset(skip).limit(
            limit).all()
    return lendings


@router.put("/lendings/{lending_id}", response_model=schemas.LendingOut)
def update_lending(lending_id: int, lending: schemas.LendingOut, db: Session = Depends(get_db),
                   current_user: models.User = Depends(get_current_user)):
    db_lending = db.query(models.Lending).filter(models.Lending.id == lending_id).first()
    if not db_lending:
        raise HTTPException(status_code=404, detail="Lending not found")

    if db_lending.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    # Обработка возврата книги
    if db_lending.return_date is None:
        book = db.query(models.Book).filter(models.Book.id == db_lending.book_id).first()
        book.available_copies += 1
        db.commit()

    for key, value in lending.dict().items():
        setattr(db_lending, key, value)
    db.commit()
    db.refresh(db_lending)
    return db_lending


@router.delete("/lendings/{lending_id}", response_model=schemas.LendingOut)
def delete_lending(lending_id: int, db: Session = Depends(get_db),
                   current_user: models.User = Depends(get_current_user)):
    db_lending = db.query(models.Lending).filter(models.Lending.id == lending_id).first()
    if not db_lending:
        raise HTTPException(status_code=404, detail="Lending not found")

    if db_lending.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    # Обработка возврата книги
    if db_lending.return_date is None:
        book = db.query(models.Book).filter(models.Book.id == db_lending.book_id).first()
        book.available_copies += 1
        db.commit()

    db.delete(db_lending)
    db.commit()
    return db_lending
