from fastapi import FastAPI,Response,status,HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
import time
from typing import Optional, List


from .. import models, schema, utils
from ..database import  get_db


router = APIRouter(
    prefix="/posts",
    tags = ["posts"]
)

@router.get("/", response_model=List[schema.Post])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.Post)
def create_posts(post: schema.PostCreate, db:Session= Depends(get_db)):
    new_post = models.Post(title = post.title, content = post.content, published= post.published)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.get('/{id}')
def get_post(id:int, response:Response, db: Session= Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id==id).first()
    
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"post with id :{id} not found")
    
    return {"post_detail":post}


@router.delete('/{id}')
def delete_post(id:int, db: Session=Depends(get_db)):
    deleted_post = db.query(models.Post).filter(models.Post.id==id)

    if deleted_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f" id {id} does not exist")
    
    deleted_post.delete(synchronize_session=False)
    db.commit()
    return {'message':"my post is succesfully deleted"}

@router.put('/{id}',response_model=schema.Post)
def update_post(id:int,ppost: schema.PostCreate, db:Session=Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id==id)
    updated_post = post_query.first()

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f" Post with id {id} does not exist")
    

    post_query.update(ppost.dict(), synchronize_session=False)
    db.commit()
    return {'message': post_query.first()}
