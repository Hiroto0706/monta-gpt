from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from schemas.user import UserCreate, UserResponse
from db.connection import get_db_connection
from db.crud import user as user_crud

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/{user_id}", response_model=UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db_connection)):
    db_user = user_crud.get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db_connection)):
    try:
        db_user = user_crud.create_user(db, username=user.username, email=user.email)
        if db_user is None:
            raise HTTPException(status_code=400, detail="User creation failed")
        return db_user
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
