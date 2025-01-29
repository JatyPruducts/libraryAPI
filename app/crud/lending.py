from sqlalchemy.orm import Session
from app.models import Lending
from app.schemas import LendingCreate, LendingOut


def get_lending(db: Session, lending_id: int):
    return db.query(Lending).filter(Lending.id == lending_id).first()


def get_lendings(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Lending).offset(skip).limit(limit).all()


def create_lending(db: Session, lending: LendingCreate):
    db_lending = Lending(**lending.dict())
    db.add(db_lending)
    db.commit()
    db.refresh(db_lending)
    return db_lending


def update_lending(db: Session, lending_id: int, lending: LendingOut):
    db_lending = get_lending(db, lending_id)
    if not db_lending:
        return None
    for key, value in lending.dict().items():
        setattr(db_lending, key, value)
    db.commit()
    db.refresh(db_lending)
    return db_lending


def delete_lending(db: Session, lending_id: int):
    db_lending = get_lending(db, lending_id)
    if not db_lending:
        return None
    db.delete(db_lending)
    db.commit()
    return db_lending
