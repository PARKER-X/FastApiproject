from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session


from ..database import get_db
from .. import schema, models


router = APIRouter(tags=['Authentication'])



@router.post('/login')
def login(user_credentials: schema.UserLogin, db:Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credientials")

