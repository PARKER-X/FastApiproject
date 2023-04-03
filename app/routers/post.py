from fastapi import FastAPI,Response,status,HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
import time
from typing import Optional, List


from . import models, schema, utils
from .. import  get_db


router = APIRouter()

@router.get("/posts", response_model=List[schema.Post])
def get_posts(db: Session = Depends(get_db)):
    # SQL
    # posts = cursor.execute(""" SELECT * FROM posts""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts

@router.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schema.Post)
def create_posts(post: schema.PostCreate, db:Session= Depends(get_db)):
    # Manual using list
    # post_dict = post.dict()
    # post_dict['id']  = randrange(0,1000)
    # my_posts.append(post_dict)
    # print(post)
    # return {"data":post}

    # Use Sql
    # cursor.execute(""" INSERT INTO  posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,(post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()

    new_post = models.Post(title = post.title, content = post.content, published= post.published)


    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.get('/posts/{id}')
def get_post(id:int, response:Response, db: Session= Depends(get_db)):
    # Sql
    # cursor.execute(""" SELECT * from posts WHERE id = %s """, (str(id)))
    # post = cursor.fetchone()
    # print(post)

    post = db.query(models.Post).filter(models.Post.id==id).first()
    
   

    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"post with id :{id} not found")
    
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message':f"post with id :{id} not found"}
    return {"post_detail":post}

# def find_index_post(id):
#     for i , p in enumerate(my_posts):
#         if p["id"] == id:
#             return i 

@router.delete('/posts/{id}')
def delete_post(id:int, db: Session=Depends(get_db)):
    # Manual
    # index = find_index_post(id)

    # Sql
    # cursor.execute(""" DELETE from posts WHERE id = %s RETURNING * """, (str(id)))
    # deleted_post = cursor.fetchone()
    # conn.commit()

    deleted_post = db.query(models.Post).filter(models.Post.id==id)

    if deleted_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f" id {id} does not exist")
    # my_posts.pop(index)
    deleted_post.delete(synchronize_session=False)
    db.commit()
    return {'message':"my post is succesfully deleted"}

@router.put('/posts/{id}',response_model=schema.Post)
def update_post(id:int,ppost: schema.PostCreate, db:Session=Depends(get_db)):
    # Manual
    # index = find_index_post(id)

    # Sql
    # cursor.execute(""" UPDATE posts SET title = %s , content = %s , published = %s WHERE id = %s RETURNING * """, (post.title,post.content,post.published,str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id==id)
    updated_post = post_query.first()


    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f" Post with id {id} does not exist")
    # post_dict = post.dict()
    # post_dict['id'] = id
    # my_posts[index] = post_dict

    post_query.update(ppost.dict(), synchronize_session=False)
    db.commit()
    return {'message': post_query.first()}
