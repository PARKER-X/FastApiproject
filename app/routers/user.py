from fastapi import FastAPI,Response,status,HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
import time
from typing import Optional, List


from . import models, schema, utils
from .. import  get_db


router = APIRouter()


@router.post("/users", status_code=status.HTTP_201_CREATED)
def create_user(user: schema.UserCreate, db:Session=Depends(get_db)):

    # Hash the Password - user.password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)


    return new_user

@router.get('/users/{id}', response_model = schema.Userout)
def get_user(id:int,db:Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise  HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = f"User od: {id} does not exist")

    return user