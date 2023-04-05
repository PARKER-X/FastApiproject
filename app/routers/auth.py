from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session


from ..database import get_db
from .. import schema, models, utils , oauth2

router = APIRouter(tags=['Authentication'])



@router.post('/login')
def login(user_credentials: schema.UserLogin, db:Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credientials")
    
    if not utils.verify(user_credentials.password , user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,  detail=f"Invalid Credientials")
    
    #create a token
    # return a token

    access_token = oauth2.create_access_token(data= {"user_id":user.id})

    return {"access_token":access_token, "token_type":"bearer"}


