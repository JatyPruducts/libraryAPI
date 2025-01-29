from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas, models
from app.database import get_db
from app.utils.auth import get_current_user, get_admin_user, create_access_token

router = APIRouter()


@router.post("/users/", response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db),
                current_user: models.User = Depends(get_admin_user)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db=db, user=user)


@router.get("/users/me", response_model=schemas.UserOut)
def read_users_me(current_user: models.User = Depends(get_current_user)):
    return current_user


@router.put("/users/{user_id}", response_model=schemas.UserOut)
def update_user(user_id: int, user: schemas.UserOut, db: Session = Depends(get_db),
                current_user: models.User = Depends(get_current_user)):
    if current_user.id != user_id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    updated_user = crud.update_user(db=db, user_id=user_id, user=user)
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user
