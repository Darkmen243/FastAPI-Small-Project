from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import crud
import schemas
from typing import List

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/create_user", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)

@router.get("/{user_id}", response_model=schemas.UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.get("/", response_model=List[schemas.UserResponse])
def get_users(skip:int=0,limit:int=100,db:Session=Depends(get_db)):
    users = crud.get_users(db,skip=skip,limit=limit)
    return users