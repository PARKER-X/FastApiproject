from fastapi import FastAPI,Response,status,HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session

from . import models
from .database import engine, SessionLocal


models.Base.metadata.create_all(bind=engine)


app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




class Post(BaseModel):
    title: str 
    content: str
    published: bool = True
    # rating: Optional[int] = None


# Database Connection
try:
    conn = psycopg2.connect(host="localhost", database='fastapi', user='postgres', password = 'password123', cursor_factory = RealDictCursor)
    cursor = conn.cursor()
    print("Database connection was succesfull!")
except Exception as error:
    print("Failed to connect database")
    print("Error:",error)



my_posts = []

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p
        
@app.get('/')
async def root():
    context = {"message":"Hello World"}
    return context


@app.get("/sqlalchemy")
def tests_posts(db: Session = Depends(get_db)):
    return {"data":"success"}


@app.get("/posts")
def get_posts():
    posts = cursor.execute(""" SELECT * FROM posts""")
    posts = cursor.fetchall()
    print(posts)
    return {"data":posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    # post_dict = post.dict()
    # post_dict['id']  = randrange(0,1000)
    # my_posts.append(post_dict)
    # print(post)
    # return {"data":post}

    # Use Sql
    cursor.execute(""" INSERT INTO  posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,(post.title, post.content, post.published))
    new_post = cursor.fetchone()

    conn.commit()

    return {"data":new_post}


@app.get('/posts/{id}')
def get_post(id:int, response:Response):
    cursor.execute(""" SELECT * from posts WHERE id = %s """, (str(id)))
    post = cursor.fetchone()
    # print(post)
    
   

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

@app.delete('/posts/{id}')
def delete_post(id:int):
    # index = find_index_post(id)
    cursor.execute(""" DELETE from posts WHERE id = %s RETURNING * """, (str(id)))
    deleted_post = cursor.fetchone()
    conn.commit()

    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f" id {id} does not exist")
    # my_posts.pop(index)
    return {'message':"my post is succesfully deleted"}

@app.put('/posts/{id}')
def update_post(id:int,post: Post):
    # index = find_index_post(id)
    cursor.execute(""" UPDATE posts SET title = %s , content = %s , published = %s WHERE id = %s RETURNING * """, (post.title,post.content,post.published,str(id)))
    updated_post = cursor.fetchone()
    conn.commit()

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f" Post with id {id} does not exist")
    # post_dict = post.dict()
    # post_dict['id'] = id
    # my_posts[index] = post_dict
    return {'message': updated_post}


